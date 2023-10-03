package HW01;

import ij.IJ;
import ij.ImagePlus;

import java.io.File;
import java.nio.file.Paths;

public class Main {

    public static void main(String[] args) {
        Task1 task1 = new Task1();
        task1.run("");


        String imagePath = "/Users/mrnobody/IdeaProjects/HW01/src/main/java/HW01/image.png";
        ImagePlus ip = IJ.openImage(imagePath);

        Task2 task2 = new Task2();
        task2.run(ip.getProcessor());
        task2.setup("", ip);


    }
}

