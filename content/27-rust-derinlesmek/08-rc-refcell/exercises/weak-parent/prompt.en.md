`struct Node { name: String, parent: RefCell<Weak<Node>> }` is ready. Write `fn parent_name(node: &Node) -> Option<String>`: the parent's name if it lives, otherwise `None`.
