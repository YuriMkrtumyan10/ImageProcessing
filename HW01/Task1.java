package HW01;

import ij.IJ;
import ij.ImagePlus;
import ij.process.ImageProcessor;
import ij.process.ByteProcessor;
import ij.plugin.PlugIn;

import java.io.*;

public class Task1 implements PlugIn{
    private int getTotalOfCourses(String crsFilePath) {
        int N = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(crsFilePath))) {
            while (br.readLine() != null) {
                N++;
            }
        } catch (IOException e) {
            IJ.error("Error reading *.crs file: " + e.getMessage());
        }
        return N;
    }

    private void markClashingCourses(String stuFilePath, ImageProcessor binaryProcessor) {
        try (BufferedReader br = new BufferedReader(new FileReader(stuFilePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] tokens = line.split(" ");
                for (int i = 0; i < tokens.length - 1; i += 2) {
                    int x = Integer.parseInt(tokens[i].trim()) - 1;
                    int y = Integer.parseInt(tokens[i + 1].trim()) - 1;
                    binaryProcessor.set(x, y, 0);
                }
            }
        } catch (IOException e) {
            IJ.error("Error reading *.stu file: " + e.getMessage());
        }
    }

    public void run(String args) {
        String crsFilePath = "/Users/mrnobody/IdeaProjects/HW01/src/main/java/HW01/pur-s-93.crs";
        String stuFilePath = "/Users/mrnobody/IdeaProjects/HW01/src/main/java/HW01/pur-s-93.stu";

        int N = getTotalOfCourses(crsFilePath);
        ImageProcessor binaryProcessor = new ByteProcessor(N, N);

        binaryProcessor.setValue(255);
        binaryProcessor.fill();

        markClashingCourses(stuFilePath, binaryProcessor);

        ImagePlus resultImage = new ImagePlus("Course Scheduler", binaryProcessor);
        String outputPath = "/Users/mrnobody/IdeaProjects/HW01/src/main/java/HW01/image.png";
        IJ.save(resultImage, outputPath);
        IJ.log("Image saved as " + outputPath);
        resultImage.show();
    }
}
