from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import logging
import csv
from tkinter import filedialog


class Kymograph:

    def __init__(self, column_range: int = 10):
        self.column_range = column_range

        # Configure logging for the class
        logging.basicConfig(filename='kymograph.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def flatten(image_data) -> np.ndarray:
        columns = image_data.shape[1]
        averages = []

        for i in range(columns):
            column_average = image_data[:, i].mean()
            averages.append(column_average)

        return np.asarray(averages)

    def max_increase_column(self, averages) -> int:
        max_increase = -np.inf
        max_increase_start_column = -1

        for i in range(len(averages) - self.column_range):
            current_sum = sum(averages[i:i + self.column_range])

            if i > 0:
                previous_sum = sum(averages[i - 1:i + self.column_range - 1])
                increase = current_sum - previous_sum
                if increase > max_increase:
                    max_increase = increase
                    max_increase_start_column = i - 1

        return max_increase_start_column

    def save_to_csv(self, image_folder: str, csv_filename: str = "results.csv"):
        """
        Saves the average intensity data of all images to a csv file.

        :param image_folder:
        :param csv_filename: the name of the csv file to write to.
        """

        # Check if there are images in the image_folder
        image_files = [file for file in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, file))]
        if not image_files:
            self.logger.error(f"No image files found in the folder: {image_folder}")
            return

        # Check if the file exists and if so, create a new file
        if os.path.isfile(csv_filename):
            base_filename, ext = os.path.splitext(csv_filename)
            i = 1
            while os.path.isfile(f"{base_filename}_{i}{ext}"):
                i += 1
            csv_filename = f"{base_filename}_{i}{ext}"

        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Write header
            header = ["Frame"]
            header.extend(image_files)
            csvwriter.writerow(header)

            max_length = 0
            image_averages = []
            # Calculate the averages for each image
            for image in image_files:
                image_path = os.path.join(image_folder, image)
                img = Image.open(image_path)  # Convert image to grayscale
                img_data = np.asarray(img)
                averages = self.flatten(img_data)
                image_averages.append(averages)
                if len(averages) > max_length:
                    max_length = len(averages)

            # Write the data
            for i in range(max_length):
                row = [i + 1]  # Frame number
                for averages in image_averages:
                    row.append(averages[i] if i < len(averages) else "")
                csvwriter.writerow(row)

        print(f"Intensity averages data saved to {csv_filename}.")

    def graph_averages(self, image: str):
        img = Image.open(image)  # convert image to grayscale
        img_data = np.asarray(img)

        averages = self.flatten(img_data)
        max_column = self.max_increase_column(averages)
        averages_2d = averages.reshape(1, -1)

        # Create a figure
        fig = plt.figure(figsize=(10, 8))
        fig.suptitle(f"Image: {os.path.basename(image)}")

        # Create the first subplot for the averages_2d image
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.imshow(averages_2d, cmap='gray')
        ax1.set_yticklabels([])  # remove y-axis labels

        # Create the second subplot for the averages plot
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(averages)
        ax2.set_title("Average Intensity")

        # Add a transparent rectangle to highlight the region of the maximum increase
        rect = patches.Rectangle((max_column, min(averages)), self.column_range, max(averages) - min(averages),
                                 linewidth=1, edgecolor='r', facecolor='r', alpha=0.5)
        ax2.add_patch(rect)

        plt.xticks(rotation=45)

        # Save the figure to the graphs directory
        plt.savefig(f"graphs/graph_{os.path.basename(image)}")

    def generate_intensity_graphs(self, image_folder: str):
        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        for image in os.listdir(image_folder):
            try:
                print(f"Processing image: {image}")
                self.logger.info(f"Processing image: {image}")
                self.graph_averages(f"{image_folder}/{image}")
            except Exception as e:
                self.logger.error(f"Failed to process image: {image}. Error: {e}")
