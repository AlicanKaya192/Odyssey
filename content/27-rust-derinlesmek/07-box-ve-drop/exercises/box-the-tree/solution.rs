enum Tree {
    Leaf(i32),
    Node(Box<Tree>, Box<Tree>),
}

fn main() {
    let t = Tree::Node(Box::new(Tree::Leaf(1)), Box::new(Tree::Leaf(2)));
    if let Tree::Node(_, _) = t {
        println!("node");
    }
}
