from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Grid, Point, VectorDicts
from typing import List, Dict

files = get_txt_files(__file__)
#########
# Start #
#########

class GardenRegion:
    def __init__(self, initial_plot: GardenPlot, grid: Grid):         
        self.plots: List[GardenPlot] = []
        self.area = 0
        self.perimiter = 0
        self.price = 0 
        self.neighbours = set()
        initial_neihbours = initial_plot.position.neighbours(include_diagonals=False, include_self=False)
        initial_neihbours = [x for x in initial_neihbours  if grid.valid_location(x)]
        self.add_neighbours(initial_plot, initial_neihbours)
        self.add_plot(initial_plot, grid)
        self.region_type = self.plots[0].plant_type

    def set_area(self):
        self.area = len(self.plots)

    def set_perimiter(self):
        for plot in self.plots:
            neighbours = plot.position.neighbours(include_diagonals=False, include_self=False)
            for neighbour in neighbours:
                if neighbour not in [x.position for x in self.plots]:
                    self.perimiter += 1

    def set_price(self):
        self.price = self.area * self.perimiter

    def add_neighbours(self, plot: GardenPlot, neighbours: List[Point]):        
        if not self.neighbours:
            self.neighbours = set(neighbours)
        else:
            # append to self.neighbours only the points that are not already in self.neighbours
            self.neighbours = self.neighbours.union(set(neighbours))
        
        # if plot in self.neighbours remove from self.neighbours
        if plot.position in self.neighbours:
            self.neighbours.remove(plot.position)        
        # remove neighbours that are already in self.plots
        self.neighbours = self.neighbours.difference(set([plot.position for plot in self.plots]))
            
                        
    def add_plot(self, plot: GardenPlot, grid: Grid):
        plot_neighbours = plot.position.neighbours(include_diagonals=False, include_self=False)
        plot_neighbours = [x for x in plot_neighbours  if grid.valid_location(x)]
        if any(plot_neighbour in [plot.position for plot in self.plots] for plot_neighbour in plot_neighbours):
            self.plots.append(plot)            
            self.add_neighbours(plot, plot_neighbours)
        elif not self.plots:
            self.plots.append(plot)
            self.add_neighbours(plot, plot_neighbours)

class GardenPlot:
    def __init__(self, plant_type: str, position: Point):
        self.plant_type = plant_type
        self.position = position

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [list(x) for x in self.input]        
        self.grid = Grid(self.input_parsed)
        self.plots = [GardenPlot(self.grid.value_at_point(x),x) for x in self.grid._all_points]
        self.regions = self.add_to_region()
        self.aggregate_neighbouring_regions_of_same_region_type()

    def add_to_region(self):
        regions: List[GardenRegion] = []
        for plot in self.plots:
            # find a GardenRegion in regions that has the same region_type as plot.plant_type and is neighbour to plot
            # if a region was found add the plot to the region
            # else create a new region and add the plot to it
            region = next((x for x in regions if x.region_type == plot.plant_type and plot.position in x.neighbours), None)
            if region:
                region.add_plot(plot, self.grid)
            else:
                new_region = GardenRegion(plot, self.grid)
                regions.append(new_region)
        return regions
    
    def aggregate_neighbouring_regions_of_same_region_type(self):
        for region in self.regions:
            region_neighbours = [x for x in self.regions if x.region_type == region.region_type and x != region]
            for neighbour in region_neighbours:
                if any(plot.position in region.neighbours for plot in neighbour.plots):
                    region.plots.extend(neighbour.plots)
                    region.neighbours = region.neighbours.union(neighbour.neighbours)
                    region.neighbours = region.neighbours.difference(set([plot.position for plot in self.plots]))
                    self.regions.remove(neighbour)
                    break   


    def calc_areas(self):
        for region in self.regions:
            region.set_area()

    def calc_perimiters(self):
        for region in self.regions:
            region.set_perimiter()

    def calc_prices(self):
        for region in self.regions:
            region.set_price()

    def solve(self, part):
        if part == 1:
            self.calc_areas()
            self.calc_perimiters()
            self.calc_prices()
            return sum([x.price for x in self.regions])
        elif part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 140
    assert main(raw=files["test2"], part=1) == 772
    assert main(raw=files["test3"], part=1) == 1930
    assert main(raw=files["test4"], part=1) == 280
    # assert main(raw=files["test"], part=2) == 81
    

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 717
    # assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
