## A table

| Type | Owner | For |
|---|---|---|
| `&T`, `&mut T` | None, a borrow | Most work |
| `Box<T>` | One | Heap, recursion, `dyn` |
| `Rc<T>` | Many, a single thread | Sharing (section 08) |
| `Arc<T>` | Many, across threads | Sharing (section 11) |
| `RefCell<T>` | One, checked at run time | Interior mutability |
| `String`, `Vec<T>` | One | Growing data |

## Box forms

| Job | Written |
|---|---|
| Create | `Box::new(5)` |
| Take the value | `*boxed` |
| Change | `*boxed = 6` (with `mut`) |
| A method | `boxed.len()` (through deref) |
| Take out the inside | `*boxed` (`T` moves) |

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `E0072` | A type of endless size | Add `Box` |
| `E0040` | A call of `x.drop()` | `drop(x)` |
| `E0382` | Use after `drop(x)` | Change the order |
| `E0614` | A type `*` cannot apply to | Write `Deref` |

## Copy and Drop

A type cannot have both: if a value doing work on deletion were copied, the work would be done twice.
