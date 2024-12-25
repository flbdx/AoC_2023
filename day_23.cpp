#include <cstdlib>
#include <cstdio>
#include <cstdint>
#include <cinttypes>

#include <sstream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <list>
#include <utility>
#include <algorithm>

const char *test_input = R"DELIM(#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#)DELIM";

// wrapper over a std::vector<bool> used to represent the visited nodes
struct Visited {
    std::vector<bool> v;

    Visited(Visited &&o) : v(std::move(o.v)) {}
    Visited(size_t w, size_t h): v(w*h) {}
    Visited(size_t w, size_t h, int32_t bit): v(w*h) {
        v[bit] = true;
    }
    Visited(const Visited &o) : v(o.v) {}
    Visited(const Visited &o, int32_t bit) : v(o.v) {
        v[bit] = true;
    }
    
};

static size_t work_p2(std::istream &in) {
    int32_t width = 0;
    int32_t height = 0;
    typedef std::pair<int32_t, int32_t> Point;
    std::map<Point, char> graph;

    {
        int32_t y = 0;
        for (std::string line; std::getline(in, line); ) {
            if (line.size() == 0) {
                break;
            }
            int32_t x = 0;
            for (char c : line) {
                graph[Point{x, y}] = c;
                x += 1;
            }
            width = x;
            y += 1;
        }
        height = y;
    }

    auto point_to_bit = [&width](const Point &p) -> int32_t {
        return p.second * width + p.first;
    };

    std::vector<bool> walls;        // bitset with the walls
    walls.resize(width * height);

    for (int32_t y = 0; y < height; ++y) {
        for (int32_t x = 0; x < width; ++x) {
            if (graph.at(Point{x,y}) == '#') {
                walls[point_to_bit(Point{x,y})] = true;
            }
        }
    }

    typedef std::pair<Point, Visited > QueueType;
    std::list<QueueType> queue;
    Point start {1,0};
    Point end {width - 2, height - 1};
    queue.emplace_back(start, Visited{size_t(width), size_t(height), point_to_bit(start)});

    size_t best = 0;

    std::vector<Point> directions {Point{1,0}, Point{-1,0}, Point{0,1}, Point{0,-1}};

    while (!queue.empty()) {
        const QueueType &q = queue.back();  // reference on back, don't pop now()
        const auto &p = q.first;
        const auto &visited = q.second;

        if (q.first == end) {
            size_t l = std::count(q.second.v.begin(), q.second.v.end(), true);
            if (l > best) {
                best = l;
                printf("%zu\n", best-1);
            }
            queue.pop_back();
            continue;
        }

        for (const auto &d : directions) {
            Point np {p.first + d.first, p.second + d.second};
            if (np.first < 0 || np.first >= width || np.second < 0 || np.second >= height) {
                continue;
            }
            int32_t npb = point_to_bit(np);
            if (walls.at(npb) || visited.v.at(npb)) {
                continue;
            }
            // emplace before back()
            queue.emplace(std::prev(queue.end()), np, Visited{visited, npb});
        }
        queue.pop_back();
    }

    return best-1;
}


int main() {
    std::string test_input_s = test_input;
    std::istringstream iss_test(test_input_s);
    std::ifstream in("input_23");

    if (work_p2(iss_test) != 154) {
        fprintf(stderr, "Error: test part 2\n");
        return 1;
    }

    printf("%zu\n", work_p2(in));

    return 0;    
}