import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from PIL import Image
import numpy as np
from kymograph import Kymograph

class TestKymograph(unittest.TestCase):
    def setUp(self):
        # Prepare the image_folder with some sample images
        self.image_folder = "test_images"
        os.makedirs(self.image_folder, exist_ok=True)
        data = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        for i in range(5):
            img = Image.fromarray(data)
            img.save(os.path.join(self.image_folder, f"image_{i}.png"))

        # Create an instance of Kymograph
        self.kymograph = Kymograph()

    def tearDown(self):
        # Clean up the created folder after tests
        for file in os.listdir(self.image_folder):
            os.remove(os.path.join(self.image_folder, file))
        os.rmdir(self.image_folder)

        # Delete the created csv file if exists
        if os.path.exists("results.csv"):
            os.remove("results.csv")

    def test_save_to_csv(self):
        self.kymograph.save_to_csv(self.image_folder, "results.csv")

        # Assert the csv file is created
        self.assertTrue(os.path.exists("results.csv"))

        # Open the csv file
        data_frame = pd.read_csv("results.csv")

        # Go through each image file and compare the averages
        for image_file in os.listdir(self.image_folder):
            img = Image.open(os.path.join(self.image_folder, image_file))
            img_data = np.array(img)
            expected_averages = self.kymograph.flatten(img_data)

            # Compare with the data in the CSV
            csv_averages = data_frame[image_file].dropna().values
            self.assertTrue(np.allclose(csv_averages, expected_averages))

if __name__ == '__main__':
    unittest.main()
