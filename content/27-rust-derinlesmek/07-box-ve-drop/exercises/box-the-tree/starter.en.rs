enum Tree {
    Leaf(i32),
    Node(Tree, Tree),
}

fn main() {
    let t = Tree::Node(Tree::Leaf(1), Tree::Leaf(2));
    if let Tree::Node(_, _) = t {
        println!("node");
    }
}
