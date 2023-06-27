from kymograph import Kymograph
from gui import GUI

graph = Kymograph(
    column_range=10,
)

images_folder = "images"


def main():
    graph.generate_intensity_graphs(images_folder)
    # graph.save_to_csv(images_folder, csv_filename="results.csv")


if __name__ == "__main__":
    main()
    # GUI().run()
