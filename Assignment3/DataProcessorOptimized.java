import java.util.ArrayList;
import java.util.List;

public class DataProcessorOptimized {

    public static void main(String[] args) {
        // Initializing the data list with some sample data
        List<String> data = new ArrayList<>();
        data.add("Hello");
        data.add("World");
        data.add("Java");
        data.add("Performance");
        data.add("Optimization");

        // Creating an instance of DataProcessorOptimized and processing the data
        DataProcessorOptimized processor = new DataProcessorOptimized();
        processor.processData(data);
    }

    public void processData(List<String> data) {
        // Using StringBuilder for efficient string concatenation
        StringBuilder result = new StringBuilder();

        // Iterating through each item in the data list
        for (String item : data) {
            // Appending the item to the StringBuilder
            result.append(item);
        }

        // Converting StringBuilder to String and performing further processing
        furtherProcessing(result.toString());
    }

    private void furtherProcessing(String result) {
        // Placeholder for further processing of the result
        System.out.println("Processed result: " + result);
    }
}
