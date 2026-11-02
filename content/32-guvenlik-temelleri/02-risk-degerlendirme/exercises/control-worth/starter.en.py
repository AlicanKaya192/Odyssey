def control_worth(ale_before, ale_after, annual_cost):
    net = ale_before - ale_after
    return (net, net > 0)

print(control_worth(20000, 4000, 5000))
print(control_worth(3000, 1000, 2500))
