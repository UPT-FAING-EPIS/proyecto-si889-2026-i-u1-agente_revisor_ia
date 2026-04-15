create extension if not exists vector;
create extension if not exists pgcrypto;

create table if not exists public.documents (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  filename text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.document_chunks (
  id bigserial primary key,
  document_id uuid not null references public.documents(id) on delete cascade,
  content text not null,
  embedding vector(3072) not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_documents_user_id on public.documents(user_id);
create index if not exists idx_document_chunks_document_id on public.document_chunks(document_id);

create index if not exists idx_document_chunks_embedding
  on public.document_chunks
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

create or replace function public.match_document_chunks(
  match_document_id uuid,
  query_embedding vector(3072),
  match_count integer default 5
)
returns table (
  id bigint,
  document_id uuid,
  content text,
  similarity double precision
)
language sql
stable
set search_path = public
as $$
  select
    c.id,
    c.document_id,
    c.content,
    1 - (c.embedding <=> query_embedding) as similarity
  from public.document_chunks c
  where c.document_id = match_document_id
  order by c.embedding <=> query_embedding
  limit match_count;
$$;

alter table public.documents enable row level security;
alter table public.document_chunks enable row level security;

drop policy if exists documents_select_own on public.documents;
create policy documents_select_own
  on public.documents
  for select
  using ((select auth.uid()) = user_id);

drop policy if exists documents_insert_own on public.documents;
create policy documents_insert_own
  on public.documents
  for insert
  with check ((select auth.uid()) = user_id);

drop policy if exists documents_update_own on public.documents;
create policy documents_update_own
  on public.documents
  for update
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

drop policy if exists documents_delete_own on public.documents;
create policy documents_delete_own
  on public.documents
  for delete
  using ((select auth.uid()) = user_id);

drop policy if exists chunks_select_owner on public.document_chunks;
create policy chunks_select_owner
  on public.document_chunks
  for select
  using (
    exists (
      select 1
      from public.documents d
      where d.id = document_chunks.document_id
        and d.user_id = (select auth.uid())
    )
  );

drop policy if exists chunks_insert_owner on public.document_chunks;
create policy chunks_insert_owner
  on public.document_chunks
  for insert
  with check (
    exists (
      select 1
      from public.documents d
      where d.id = document_chunks.document_id
        and d.user_id = (select auth.uid())
    )
  );

drop policy if exists chunks_delete_owner on public.document_chunks;
create policy chunks_delete_owner
  on public.document_chunks
  for delete
  using (
    exists (
      select 1
      from public.documents d
      where d.id = document_chunks.document_id
        and d.user_id = (select auth.uid())
    )
  );
