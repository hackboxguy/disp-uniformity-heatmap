#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse
import sys
import csv

# Use a non-interactive backend to avoid GUI requirements
matplotlib.use('Agg')

def parse_resolution(resolution_str):
    try:
        width, height = map(int, resolution_str.lower().split("x"))
        return width, height
    except ValueError:
        raise argparse.ArgumentTypeError("Resolution must be in the format WIDTHxHEIGHT (e.g., 1920x1080)")

def save_csv(csvfile, percent_diff, gridx, gridy):
    with open(csvfile, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header (column labels)
        #writer.writerow([f"Column {i+1}" for i in range(gridx)])
        # Write grid values
        for row in percent_diff:
            writer.writerow(row)
    print(f"CSV file saved to: {csvfile}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Process brightness uniformity heatmap of an input jpg photo of a display showing full white pattern.",
        epilog="Example usage: python disp-uniformity-heatmap.py --infile=/path/to/input.jpg --outfile=/path/to/output.jpg --outfileresolution=1920x1080",
    )
    parser.add_argument("--infile", type=str, required=True, help="Path to the input JPG image file")
    parser.add_argument("--outfile", type=str, help="Path to save the output JPG image file")
    parser.add_argument(
        "--outfileresolution", 
        type=parse_resolution, 
        default="1920x1080", 
        help="Resolution of the output file in the format WIDTHxHEIGHT (default: 1920x1080)"
    )
    parser.add_argument("--gridx", type=int, default=80, help="Number of grid columns (default: 80)")
    parser.add_argument("--gridy", type=int, default=45, help="Number of grid rows (default: 45)")
    parser.add_argument("--textsize", type=int, default=8, help="Text size for grid markers (default: 8)")
    parser.add_argument("--csvfile", type=str, help="Path to save the CSV file with grid data")

    # Show help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Check if at least one output argument is provided
    if not args.outfile and not args.csvfile:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Step 1: Load the Image and Convert to Grayscale
    image = cv2.imread(args.infile)
    if image is None:
        print(f"Error: Unable to load the image from path: {args.infile}")
        return
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Automatically Crop the White Rectangle (Assume it’s the brightest area)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    display_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(display_contour)
    cropped_display = gray[y:y+h, x:x+w]

    # Step 3: Resize for Uniformity Analysis (e.g., based on grid size)
    resized_display = cv2.resize(cropped_display, (args.gridx, args.gridy), interpolation=cv2.INTER_AREA)

    # Calculate brightness uniformity
    max_brightness = np.max(resized_display)
    percent_diff = ((resized_display / max_brightness) * 100).astype(int)

    # Step 4: Save CSV if requested
    if args.csvfile:
        save_csv(args.csvfile, percent_diff, args.gridx, args.gridy)

    # Step 5: Plot heatmap with uniformity markers (only if outfile is provided)
    if args.outfile:
        plt.figure(figsize=(args.outfileresolution[0] / 100, args.outfileresolution[1] / 100), dpi=100)
        plt.imshow(resized_display, cmap='hot', interpolation='nearest')
        plt.colorbar(label="Brightness")

        # Overlay brightness uniformity percentage markers
        for i in range(args.gridy):
            for j in range(args.gridx):
                plt.text(j, i, f"{percent_diff[i, j]}%", ha="center", va="center", color="green", fontsize=args.textsize)

        # Add title and save the heatmap as an image
        plt.title("Brightness Heatmap with Uniformity Markers")
        plt.savefig(args.outfile, format="jpg", dpi=300, bbox_inches="tight")
        print(f"Output saved to: {args.outfile}")

if __name__ == "__main__":
    main()

