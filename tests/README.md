# Test Organization
Khef's tests are split into three categories -- Interior, Perimeter, and
Exterior.

* Interior tests are unit tests. They check the behavior of the
  *interior* of the code: the parts that don't need system calls
* Perimeter tests are integration tests. They check the behavior of the
  *perimeter* of the code: the parts that do use system calls
* Exterior tests are end-to-end tests. They represent the behavior of a
  real user interacting with the code from the *outside*.

## Testing Goals
As a cryptographic tool, khef takes quality control very seriously. Much
more seriously than would be necessary if this were, say, a personal
notetaking or todo list tool. This is because incorrect use of
cryptography can give rise to situations where data *appears* to be
strongly protected, but in fact *isn't*.
