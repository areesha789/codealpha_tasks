import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class WordCounter extends JFrame implements ActionListener {

    private JTextArea textArea;
    private JButton countButton;
    private JLabel resultLabel;

    public WordCounter() {
        // Set up the frame
        setTitle("Word Counter");
        setSize(400, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Create text area
        textArea = new JTextArea();
        JScrollPane scrollPane = new JScrollPane(textArea);

        // Create button
        countButton = new JButton("Count Words");
        countButton.addActionListener(this);

        // Create label
        resultLabel = new JLabel("Words: 0");
        resultLabel.setHorizontalAlignment(SwingConstants.CENTER);

        // Add components to frame
        add(scrollPane, BorderLayout.CENTER);
        add(countButton, BorderLayout.SOUTH);
        add(resultLabel, BorderLayout.NORTH);

        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String text = textArea.getText().trim();
        if (text.isEmpty()) {
            resultLabel.setText("Words: 0");
        } else {
            String[] words = text.split("\\s+");
            resultLabel.setText("Words: " + words.length);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(WordCounter::new);
    }
}
