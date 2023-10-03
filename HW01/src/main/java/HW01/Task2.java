package HW01;
import ij.*;
import ij.process.*;
import ij.plugin.filter.PlugInFilter;

public class Task2 implements PlugInFilter {
    ImagePlus imp;

    public int setup(String arg, ImagePlus imp) {
        this.imp = imp;
        return DOES_8G;
    }

    public void run(ImageProcessor ip) {
        int width = ip.getWidth();
        int height = ip.getHeight();
        int centerX = width / 2;
        int centerY = height / 2;

        ImageProcessor leftPanel = ip.duplicate();
        leftPanel.setRoi(0, 0, centerX, height);
        leftPanel = leftPanel.crop();

        ImageProcessor rightPanel = ip.duplicate();
        rightPanel.setRoi(centerX, 0, width - centerX, height);
        rightPanel = rightPanel.crop();

        leftPanel.flipHorizontal();
        rightPanel.flipHorizontal();

        ImageProcessor topPanel = ip.duplicate();
        topPanel.setRoi(0, 0, width, centerY);
        topPanel = topPanel.crop();

        ImageProcessor bottomPanel = ip.duplicate();
        bottomPanel.setRoi(0, centerY, width, height - centerY);
        bottomPanel = bottomPanel.crop();

        topPanel.flipVertical();
        bottomPanel.flipVertical();

        ImageProcessor result = new ColorProcessor(width, height);
        result.insert(leftPanel, 0, 0);
        result.insert(rightPanel, centerX, 0);
        result.insert(topPanel, 0, 0);
        result.insert(bottomPanel, 0, centerY);

        ImagePlus modifiedImage = new ImagePlus("Modified Image", result);
        modifiedImage.show();

        String outputPath = "/Users/mrnobody/IdeaProjects/HW01/src/main/java/HW01/copy.png";
        IJ.save(modifiedImage, outputPath);
        IJ.log("Modified image saved as " + outputPath);
    }
}
