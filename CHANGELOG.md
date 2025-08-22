# Changelog

## 2025-08-20

- Integration of Django Jazzmin for a modern and customizable admin panel.
- Creative Jazzmin configuration: "cosmo" theme, custom model icons, expanded sidebar, collapsible tabs and forms,
  welcome message and branding.
- Autocomplete enabled on Book model's "Authors" field using Django native `autocomplete_fields`.
- All models and fields now have Spanish `verbose_name` and `verbose_name_plural` for better user experience in admin.
- Security configuration improvements: JWT, fail2ban, logging, and protected endpoints.
- Documentation and README updated to reflect security, authentication and deployment changes.
- Fixed Material Admin configuration issues and migrated to Jazzmin.
- Cleaned up obsolete imports and dependencies.
- Updated id fields to UUID for better security and uniqueness.
- Migrated all model primary keys from integer IDs to UUIDs for improved security and uniqueness.
- Updated all fixture files to use valid UUID values for model references.
- Fixed UUID validation errors in fixtures.

## 2025-08-21

- Added custom API endpoints to AuthorViewSet:
  - /api/authors/books_statistics/: Returns book statistics per author.
- Added custom API endpoints to BookViewSet:
  - /api/books/price_range/: Filters books by price range.
  - /api/books/advance_search/: Advanced search for books by genre, pages, and language.
- Updated tests to cover new endpoints, including:
  - Book statistics per author.
  - Price range filtering.
  - Advanced search functionality.
