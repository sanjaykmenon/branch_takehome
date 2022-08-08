Notes:
  - the address_id, user_id columns are generated during the API call.
  - These columns are used for indexing purposes. Even though UUIDs could be used as a primary key because UUIDs will end up taking more memory (16 bytes)
    as compared to INT values (4-bytes) or even big INT types (8-bytes)
  - Debugging could be more complicated, for example imagine the expression WHERE id = 'df3b7cb7-6a95-11e7-8846-b05adad3f0ae' instead of WHERE id = 5454346
  - UUIDs could also have performance issues as they are not ordered unlike INT.
