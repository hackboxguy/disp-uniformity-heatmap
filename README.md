# disp-uniformity-heatmap
Python script to digitally analyze the uneven brightness zones of a local dimming display

# Display Uniformity Calibration for Local Dimming Displays

This script is designed to calibrate the uneven uniformity zones of the displays featuring local dimming. During the manufacturing process, the script serves as an automated calibration tool that measures the uniformity of the display under test (DUT) while showing a full white pattern at maximum brightness in a dark environment.

By using a high-resolution camera to capture an image of the display, the script processes this image to generate a heatmap CSV table. This CSV table can then be stored in the display electronics as uniformity calibration data. During the operation of the local dimming display, the display uses this uniformity heatmap data as an offset to adjust the central bright dimming zones, ensuring they match the surrounding darker dimming zones for improved uniformity.

## Sample input file
![input-file](/images/input.jpg "input-file")

## Processed output file with brightness heat markers for each zone
![output-file](/images/output.jpg "output-file")

## Features

- **Heatmap Generation:** Creates a visual heatmap(jpg) that shows brightness uniformity across the display.
- **CSV Export:** Generates a CSV table containing brightness percentage values for each grid cell.
- **Resolution and Grid Customization:** Allows for customizable grid sizes and output resolution(for displays with different dimming zones).
- **Text Size Customization:** Customize text size for grid markers(for visualization).
- **Easy Integration with Display Electronics:** CSV output can be directly stored in the display’s firmware or can be translated into a binary table.

## Requirements to run disp-uniformity-heatmap.py

- Python 3.x
- OpenCV (`cv2` package)
- NumPy
- Matplotlib
- argparse
- csv

To install the necessary dependencies, run:

```bash
pip install opencv-python numpy matplotlib
```

## Usage

The script accepts various command-line arguments to customize the input and output. The user can specify the input image file, output file, grid size, text size, and CSV file for uniformity data.

### Command Line Arguments

| Argument               | Description                                                                                      | Default         |
|------------------------|--------------------------------------------------------------------------------------------------|-----------------|
| `--infile`              | Path to the input JPG image file containing the captured display pattern (required).            | N/A             |
| `--outfile`             | Path to save the output JPG image with the heatmap (optional).                                  | ./output.jpg    |
| `--csvfile`             | Path to save the CSV file with grid data (optional).                                            | N/A             |
| `--outfileresolution`   | Resolution of the output file in the format `WIDTHxHEIGHT` (optional).                          | 1920x1080       |
| `--gridx`               | Total dimming-zone-rows (optional).                                                             | 80              |
| `--gridy`               | Total dimming-zone-column (optional).                                                           | 45              |
| `--textsize`            | Text size for the grid markers (optional).                                                      | 8               |

### Example Usage

1. **Generate the Output Image (`out.jpg`) for a 80x45 dimming zone display**  
   ```bash
   python uniformity_analysis.py --infile=/path/to/input.jpg --outfile=/path/to/output.jpg --outfileresolution=1920x1080 --gridx=80 --gridy=45
   ```

2. **Generate the CSV File (`test.csv`) for a 80x45 dimming zone display**  
   ```bash
   python uniformity_analysis.py --infile=/path/to/input.jpg --csvfile=/path/to/test.csv --gridx=80 --gridy=45
   ```

3. **Generate Both Output Image(QHD) and CSV File(for default 80x45 dimming zones)**  
   ```bash
   python uniformity_analysis.py --infile=/path/to/input.jpg --outfile=/path/to/output.jpg --csvfile=/path/to/test.csv --outfileresolution=3840x2160
   ```


### Output Files

- **Output Image:** If the `--outfile` argument is provided, the script generates an image showing the heatmap of brightness uniformity. The image is saved as a JPG file.
- **CSV File:** If the `--csvfile` argument is provided, the script generates a CSV file containing brightness percentages for each grid cell. The CSV file is structured with each row representing a row of grid cells and each column representing a grid cell.

## How It Works

1. **Image Preprocessing:**  
   The input image is loaded and converted to grayscale. A threshold is applied to segment the bright regions of the image, which is assumed to be the display area showing the full white pattern.

2. **Cropping:**  
   The script automatically detects the brightest region of the image and crops the image around that area for further processing(if needed, manually cropped image can also be used as input to this script).

3. **Uniformity Analysis:**  
   The cropped image is resized into a grid based on the specified number of columns (`--gridx`) and rows (`--gridy`). Each grid cell is analyzed for brightness uniformity by calculating the brightness as a percentage of the maximum brightness in the image.

4. **Heatmap Generation:**  
   A heatmap is generated to visualize the brightness uniformity across the display.

5. **CSV Output:**  
   The brightness percentages for each grid cell are written to a CSV file, which can be used as calibration data for the display.

## Calibration Process

During manufacturing, this tool is used to generate a uniformity heatmap. The resulting CSV file can be stored within the display’s electronics, and during the operation of the local dimming display, the system will apply this data to adjust the dimming zones for consistent brightness across the screen.

## License

This script is released under the MIT License. See the `LICENSE` file for more details.
