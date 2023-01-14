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
strongly protected, but in fact *isn't*. To that end, we adhere to very
strict testing goals:

* 100% coverage of *applicable* code when running the Exterior test
  suite
  * (Exceptions raised to defend against programming errors are,
    obviously, uncheckable. They are marked as `pragma: no cover`)
* *Maximal* code coverage when running the Interior and Perimeter test
  suites

*Maximal* code coverage, in this case, means that the majority of the
code should be reachable without requiring the code to be invoked as an
application. These tests are faster to execute, and usually easier to
design and understand. In practice, that should be in the range of
85-95%. When reasonable, code that is only reachable in the Exterior
tests should be refactored into separate components that can be tested
in either Interior or Perimeter tests.
