Changelog
=========

v1.0.9 (2022-09-16)
-------------------

* Added is_spot property to the Instance class, now possible to deploy a spot instance
* Implemented __str__ method for Instance, Volume and Image Classes, now possible to print instances

v1.0.8 (2021-12-20)
-------------------

* Added ssh_key_ids property for Volume entity
* Added test coverage for ssh_key_ids

v1.0.7 (2021-10-13)
-------------------

* Fixed the previous bug in a different method

v1.0.6 (2021-10-12)
-------------------

* Fixed a bug where initializing an instance without ssh keys raises an exception

v1.0.5 (2021-09-27)
-------------------

* Added an option to set OS volume size and name on instance creation

v1.0.4 (2021-07-01)
-------------------

* Added constants documentation

v1.0.3 (2021-07-01)
-------------------

* Added missing volumes documentation

v1.0.2 (2021-06-16)
-------------------

* Added examples to documentation

v1.0.1 (2021-06-16)
-------------------

* Update version

v1.0.0 (2021-06-16)
-------------------

* Added support for storage volumes
* Breaking change: moved all constants under DataCrunchClient to DataCrunchClient.constants

v0.1.0 (2021-01-05)
-------------------

* First release, still in beta.