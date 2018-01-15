ROADMAP
=======

0.6.0 (unreleased)
------------------
- [ ] Content syndication.

0.5.0 (unreleased)
------------------
- [ ] Add Speaker model.
    - [ ] API CRUD support for Speaker model.
- [ ] Add Conference/Event model.
    - [ ] API CRUD support for Conference/Event model.

0.4.0 (unreleased)
------------------
- [ ] Add/Deploy NATS as a broker.
- [ ] Decouple rank calculation as a separate service.
- [ ] Periodically update outdated videos.

0.3.0 (unreleased)
------------------
- [ ] *add_video* command to use the API.
- [ ] *add_playlist* command to use the API.
- [ ] *rank_videos* command to use the API.
- [ ] *update_videos* command to use the API.

0.2.0 (unreleased)
------------------
- [x] Add support for coveralls.io.
    - [x] Minimum of 75% coverage.
- [ ] Read/Write public API.
    - [x] APIKey based authentication.
    - [ ] CRUD support for model Channel.
    - [ ] CRUD support for model Playlist.
    - [ ] CRUD support for model Talk.

0.1.0 (2018-01-14)
------------------
- [x] Basic listing of talks.
- [x] Detailed view of a talk.
- [x] Search talks.
- [x] Twitter Authentication.
- [x] Basic ranking algorithms.
- [x] Basic UI and templates.
- [x] Readonly public API.
- [x] Initial set of tests and documentation.