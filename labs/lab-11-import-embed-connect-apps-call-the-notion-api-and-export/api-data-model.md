# The Notion API data model (version 2025-09-03)

```
Database ──── has one or more ───▶ Data source ──── has zero or more ───▶ Page (row)
(container; inline or full page)   (schema = properties)                 (properties + content blocks)
```

| Object | Key fields | Notes |
|---|---|---|
| Database | `object: "database"`, `id`, `title`, `data_sources[] {id, name}`, `is_inline`, `in_trash`, `public_url`, `parent`, `created_time`, `last_edited_time` | Permissions are managed at the database level |
| Data source | `id`, `properties` (the schema), parent database | Use *Retrieve a data source* for the schema; query rows with `POST /data_sources/{id}/query` |
| Page | `id`, `properties`, `parent {data_source_id}`, `url` | Every row of a data source is a page |

Before September 2025 a database had exactly one data source, so the API merged the two concepts. Upgrade the
`Notion-Version` header to `2025-09-03` to receive the `data_sources` array. Integrations must be *connected* to a page or
database (⋯ → Connections) before they can read it. Source: developers.notion.com/reference/database
