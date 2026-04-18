import sys

def take_input(input_file):
    with open(input_file, "r") as file:
        lines = file.readlines()

        first_line = lines[0]
        f_l = first_line.split()
        costs = []
        for c in f_l:
            costs.append(int(c))
        cost1 = costs[0]
        cost2 = costs[1]
        cost3 = costs[2]

        field = []
        for line in lines[1:]:
            line = line.strip()
            numbers = line.split()
            int_numbers = []
            for num in numbers:
                int_numbers.append(int(num))
            field.append(int_numbers)

    return cost1, cost2, cost3, field

def calculate_cost(field, x, y, cost1, cost2, cost3):
    rows = len(field)
    cols = len(field[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    diagonal_sinkhole = False
    straight_sinkhole = False

    for direction in directions:
        dx = direction[0]
        dy = direction[1]
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < rows and ny >= 0 and ny < cols:
            if field[nx][ny] == 0:
                if dx == dy or dx == -dy:
                    diagonal_sinkhole = True
                else:
                    straight_sinkhole = True


    if straight_sinkhole:
        return cost3
    elif diagonal_sinkhole:
        return cost2
    else:
        return cost1

def find_min_cost_path(field, cost1, cost2, cost3):
    rows = len(field)
    cols = len(field[0])

    queue = []
    visited = set()

    min_cost = float('inf')
    best_path = None

    for i in range(rows):
        if field[i][0] == 1:
            initial_cost = calculate_cost(field, i, 0, cost1, cost2, cost3)
            queue.append((initial_cost, i, 0, [(i, 0)]))

    while len(queue) > 0:
        queue.sort()
        cost, x, y, path = queue.pop(0)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if y == cols - 1:
            if cost < min_cost:
                min_cost = cost
                best_path = path
            continue

        directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) not in visited and field[nx][ny] == 1:
                    step_cost = calculate_cost(field, nx, ny, cost1, cost2, cost3)
                    queue.append((cost + step_cost, nx, ny, path + [(nx, ny)]))

    return best_path, min_cost

def write_output(output_file, field, cost, path):
    with open(output_file, 'w') as file:
        if not path:
            file.write("There is no possible route!\n")
        else:
            file.write(f"Cost of the route: {cost}\n")
            output_field = []
            for row in field:
                new_row = []
                for element in row:
                    new_row.append(element)
                output_field.append(new_row)

            for x, y in path:
                output_field[x][y] = 'X'
            for row in output_field:
                row_str = ""
                for element in row:
                    row_str += str(element) + " "
                row_str = row_str.strip()
                file.write(row_str + '\n')


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    cost1, cost2, cost3, field = take_input(input_file)
    best_path, min_cost = find_min_cost_path(field, cost1, cost2, cost3)
    write_output(output_file, field, min_cost, best_path)

if __name__ == "__main__":
    main()