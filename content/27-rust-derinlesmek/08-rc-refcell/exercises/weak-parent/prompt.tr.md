`struct Node { name: String, parent: RefCell<Weak<Node>> }` hazır. `fn parent_name(node: &Node) -> Option<String>` yaz: Ebeveyn yaşıyorsa adını, değilse `None` döndürsün.
