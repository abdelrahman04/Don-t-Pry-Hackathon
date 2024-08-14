module com.giu.mpc {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.giu.mpc to javafx.fxml;
    exports com.giu.mpc;
}