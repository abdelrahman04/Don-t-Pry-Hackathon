package com.giu.mpc;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;

public class HelloApplication extends Application {
    public static int times = 0;

    @Override
    public void start(Stage stage) throws IOException {
        //create a new scene that will be displayed in the stage which contains a photo named map.png and when the photo is clicked, the exact position in the photo clicked will be displayed
        Image image = new Image(new File("map.png").toURI().toString());
        ImageView imageView = new ImageView(image);
        //set the image to be flexible with the page with the height being less than the heigh of the page by 20 pixels
        imageView.fitWidthProperty().bind(stage.widthProperty());
        imageView.fitHeightProperty().bind(stage.heightProperty().subtract(100));
        AtomicInteger xpos = new AtomicInteger();
        AtomicInteger ypos = new AtomicInteger();
        imageView.setOnMouseClicked(e -> {
            xpos.set((int) e.getX());
            ypos.set((int) e.getY());
        });
        ArrayList<String>hashs=new ArrayList<>();
        //write a code to hash the above UUID and display the hash code when the button is clicked
        Button button = new Button("Send coordinates");
        button.setOnAction(e -> {
            if (xpos.get() != 0 || ypos.get() != 0) {
                String UUID = java.util.UUID.randomUUID().toString();
                String shedUUID = hashUUID(UUID);
                hashs.add(shedUUID);
                String s = runScript("src/Server.py", (int) (xpos.get() * 100 / imageView.getImage().getWidth()), (int) (ypos.get() * 100 / imageView.getImage().getHeight()), shedUUID);
//                System.out.println("abl matba3 s" + s.length());
//                System.out.println(s);
//                System.out.println("taba3t s");
                assert s != null;
                String[] ss = s.split(" ");
//                for(var f:ss){
//                    System.out.println(f);
//                    System.out.println("ended");
//                }
                String ResultHash = ss[ss.length - 1];
                if (ResultHash.isEmpty())
                    ResultHash = " ";
                ResultHash = ResultHash.substring(0, ResultHash.length() - 1);
                if (times == 10) {
                    for(int i=0;i<hashs.size();i++){
                        String hashedUUID=hashs.get(i);
                        if (ResultHash.equals(hashedUUID)) {
                            Alert alert = new Alert(Alert.AlertType.INFORMATION);
                            alert.setTitle("User" +(i));
                            alert.setHeaderText("Contact the main headquarters immedietly");
                            alert.showAndWait();
                        } else {
                            Alert alert = new Alert(Alert.AlertType.ERROR);
                            alert.setTitle("User" +(i+1));
                            alert.setHeaderText("it's not you");
                            alert.showAndWait();
                        }
                    }
                }
            } else {
                //show an alert if the user didn't click on the photo
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("Error");
                alert.setHeaderText("You didn't click on the photo");
                alert.showAndWait();
            }

        });
        BorderPane pane = new BorderPane();
        pane.setCenter(imageView);
        pane.setBottom(button);
        Scene scene = new Scene(pane);
        stage.setScene(scene);
        stage.show();
    }

    private String hashUUID(String uuid) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(uuid.getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        launch();
    }

    public static String runScript(String source, int x, int y, String name) {
        // The command to run the Python script
        List<String> command = new ArrayList<>();
        command.add("python3");
        command.add(source);
        command.add(String.valueOf(x));
        command.add(String.valueOf(y));
        command.add(name);
        command.add(String.valueOf(++times));

        try {
            // Print the command for debugging
            System.out.println("Running command: " + String.join(" ", command));

            ProcessBuilder processBuilder = new ProcessBuilder(command);
            // Start the process
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));

            String line;
            StringBuilder output = new StringBuilder();
            StringBuilder errorOutput = new StringBuilder();

            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            while ((line = errorReader.readLine()) != null) {
                errorOutput.append(line).append("\n");
            }

            int exitCode = process.waitFor();

            System.out.println("Exited with code: " + exitCode);
            System.out.println("Output: " + output);
            if (errorOutput.length() > 0) {
                System.out.println("Errors: " + errorOutput);
            }

            return output.toString();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }
}





