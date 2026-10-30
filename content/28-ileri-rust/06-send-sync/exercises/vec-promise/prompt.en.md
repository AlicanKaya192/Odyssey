`MyVec<T>` does not pass to a branch because it holds `NonNull`. Write `Send` with `T: Send`, and `Sync` with `T: Sync`. Add a `// SAFETY:` comment.
