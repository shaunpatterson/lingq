package org.lingq;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JToggleButton;
import javax.swing.border.EmptyBorder;
import javax.ws.rs.core.MultivaluedMap;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.core.util.MultivaluedMapImpl;

public class Generate extends JFrame {

	private JPanel contentPane;
	private JTextField apiField;
	private JTextField outputField;
	private JToggleButton statusButton1; 
	private JToggleButton statusButton2; 
	private JToggleButton statusButton3; 
	private JToggleButton statusButton4;
	
	private static final int WIDTH = 600;
	private static final int HEIGHT = 400;
	private JTextField langField;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Generate frame = new Generate();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	private List<LingQ> getLingQs() {
		Client client = Client.create();
		WebResource webResource = client.resource("http://www.lingq.com/api_v2/" + langField.getText() + "/lingqs/");
		
		MultivaluedMap<String, String> queryParams = new MultivaluedMapImpl();
		queryParams.add("apikey", apiField.getText());
		
		ClientResponse response = webResource.queryParams(queryParams).accept("application/json")
											 .get(ClientResponse.class);
		if (response.getStatus() != 200) {
			System.out.println("Fail");
			JOptionPane.showMessageDialog(this, "Failed to pull LingQs");
			
			return null;
		} else {
			String json = response.getEntity(String.class);
			
			// Deserialize
			Type listType = new TypeToken<List<LingQ>>(){}.getType();
			List<LingQ> lingqs = new Gson().fromJson(json, listType);
			
			System.out.println("Num LingQs pulled: " + lingqs.size());
			return lingqs;
		}
	}
	
	private void generate() {
		if (apiField.getText() == null || apiField.getText().length() == 0 ||
			langField.getText() == null || langField.getText().length() == 0 ||
			outputField.getText() == null || outputField.getText().length() == 0) 
		{
			JOptionPane.showMessageDialog(this, "You must fill out all fields");
			return;
		}

		JOptionPane.showMessageDialog(this, "This may take some time.  Be patient!");
		
		System.out.println("Generating...");
		List<LingQ> lingqs = getLingQs();
		if (lingqs == null) {
			return;
		}
		
		// Strip out the LingQs with unwanted status (wish you could do this with the API...)
		List<LingQ> desiredLingQs = new ArrayList<LingQ>();
		for (LingQ l : lingqs) {
			boolean keep = false;
			
			keep = keep || (l.getStatus() == 0 && statusButton1.isSelected());
			keep = keep || (l.getStatus() == 1 && statusButton2.isSelected());
			keep = keep || (l.getStatus() == 2 && statusButton3.isSelected());
			keep = keep || (l.getStatus() == 3 && statusButton4.isSelected());
			
			if (keep) {
				desiredLingQs.add(l);
			}
		}
		
		JOptionPane.showMessageDialog(this, "Successfully pulled " + desiredLingQs.size() + " LingQs. Now we'll generate the images.  \n\nThis could take several minutes.  \n\nYou'll see another popup message when processing is finished");
		
		setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
		
		int i = 0;
		for (LingQ l : desiredLingQs) {
			String fileName = outputField.getText() +
							  System.getProperty("file.separator") + i + ".png";
			generatePicture(fileName, l);
			i++;
		}

		setCursor(Cursor.getDefaultCursor());
		
		JOptionPane.showMessageDialog(this, "All done");
	}
	
	private Font determineFont(Graphics2D g, String text, int maxLength, int defaultSize) 
	{
		Font font = null;
		int fontSize = defaultSize;
		while(true) {		
			font = new Font("Arial", Font.BOLD, fontSize);
			g.setFont(font);
			
			FontMetrics metric = g.getFontMetrics();
			int stringWidth = metric.stringWidth(text);
			
			if (stringWidth < maxLength) {
				// Good to go
				break;
			} 
			
			// Try decreasing the font size slightly
			fontSize--;
			
			if (fontSize == 1) {
				// Give up
				break;
			}
		} 

		return font;
	}
	
	private void generatePicture(final String fileName, final LingQ lingq) {
		BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_ARGB);  
		Graphics2D g = image.createGraphics();
		
		g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
		
		g.setColor(new Color(255, 250, 240));
		g.fillRect(0, 0, WIDTH, HEIGHT);
		
		g.setColor(Color.BLACK);
	
		/*
		 * Draw the term
		 */
		Font font = determineFont(g, lingq.getTerm(), (WIDTH - (WIDTH / 8)), 40);
		g.setFont(font);
		
		FontMetrics metric = g.getFontMetrics();
		int stringWidth = metric.stringWidth(lingq.getTerm());
		
		g.drawString(lingq.getTerm(), (WIDTH - stringWidth) / 2, 75);
	
		// Break
		int xMargin = (WIDTH - (WIDTH / 8));
		g.drawLine(xMargin, 100, WIDTH - xMargin, 100);
		
		/*
		 * Draw the hint
		 */
		font = determineFont(g, lingq.getHint(), (WIDTH - (WIDTH / 8)), 40);
		g.setFont(font);
		
		metric = g.getFontMetrics();
		stringWidth = metric.stringWidth(lingq.getHint());
		
		g.drawString(lingq.getHint(), (WIDTH - stringWidth) / 2, 160);
		
		/*
		 * Finally draw the phrase 
		 */
		font = determineFont(g, lingq.getFragment(), (WIDTH - (WIDTH / 8)), 25);
		g.setFont(font);
		
		metric = g.getFontMetrics();
		stringWidth = metric.stringWidth(lingq.getFragment());
		
		g.drawString(lingq.getFragment(), (WIDTH - stringWidth) / 2, 375);
		
		
		try {
			ImageIO.write(image, "PNG", new File(fileName));
		} catch (Exception e) { }
	}
	
	private void chooseOutputButtonClicked() {
		JFileChooser chooser = new JFileChooser();
	    chooser.setCurrentDirectory(new java.io.File("."));
	    chooser.setDialogTitle("Choose output directory");
	    chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	    chooser.setAcceptAllFileFilterUsed(false);
	    
	    if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) { 
	    	outputField.setText(chooser.getSelectedFile().toString());
	    }
	}

	/**
	 * Create the frame.
	 */
	public Generate() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 514, 395);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblYourApiKey = new JLabel("Your API Key");
		lblYourApiKey.setBounds(12, 8, 134, 15);
		contentPane.add(lblYourApiKey);
		
		apiField = new JTextField();
		apiField.setBounds(144, 6, 353, 19);
		contentPane.add(apiField);
		apiField.setColumns(10);
		
		JLabel lblNewLabel = new JLabel("Output Directory");
		lblNewLabel.setBounds(12, 69, 134, 15);
		contentPane.add(lblNewLabel);
		
		outputField = new JTextField();
		outputField.setColumns(10);
		outputField.setBounds(144, 67, 287, 19);
		contentPane.add(outputField);
		
		JButton button = new JButton("...");
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				chooseOutputButtonClicked();
			}
		});
		button.setBounds(443, 69, 54, 15);
		contentPane.add(button);
		
		statusButton1 = new JToggleButton("1");
		statusButton1.setSelected(true);
		statusButton1.setBounds(12, 132, 43, 25);
		contentPane.add(statusButton1);
		
		JLabel lblPullWordsWith = new JLabel("Pull words with status of:");
		lblPullWordsWith.setBounds(12, 105, 176, 15);
		contentPane.add(lblPullWordsWith);
		
		statusButton2 = new JToggleButton("2");
		statusButton2.setSelected(true);
		statusButton2.setBounds(67, 132, 43, 25);
		contentPane.add(statusButton2);
		
		statusButton3 = new JToggleButton("3");
		statusButton3.setSelected(true);
		statusButton3.setBounds(122, 132, 43, 25);
		contentPane.add(statusButton3);
		
		statusButton4 = new JToggleButton("4");
		statusButton4.setSelected(true);
		statusButton4.setBounds(177, 132, 43, 25);
		contentPane.add(statusButton4);
		
		JButton btnGenerate = new JButton("Generate");
		btnGenerate.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				generate();
			}
		});
		btnGenerate.setBounds(12, 186, 116, 25);
		contentPane.add(btnGenerate);
		
		JLabel lblSourceAtGithubcomspattersonlingq = new JLabel("Source at: github.com/spatterson/lingq");
		lblSourceAtGithubcomspattersonlingq.setBounds(12, 223, 294, 15);
		contentPane.add(lblSourceAtGithubcomspattersonlingq);
		
		JLabel lblLanguageCode = new JLabel("Language Code");
		lblLanguageCode.setBounds(12, 35, 116, 15);
		contentPane.add(lblLanguageCode);
		
		langField = new JTextField();
		langField.setColumns(10);
		langField.setBounds(144, 36, 353, 19);
		contentPane.add(langField);
		
		JLabel lblUseAtYour = new JLabel("Use at your own risk!");
		lblUseAtYour.setBounds(12, 340, 227, 15);
		contentPane.add(lblUseAtYour);
		
		JLabel lblIWouldntOutput = new JLabel("I wouldn't output directly to a memory card.  ");
		lblIWouldntOutput.setBounds(12, 250, 420, 15);
		contentPane.add(lblIWouldntOutput);
		
		JLabel lblTheyCanBe = new JLabel("They can be very slow.");
		lblTheyCanBe.setBounds(12, 266, 420, 15);
		contentPane.add(lblTheyCanBe);
		
		JLabel lblNewLabel_1 = new JLabel("Output to local machine and manually copy the files to the card.");
		lblNewLabel_1.setBounds(12, 286, 485, 15);
		contentPane.add(lblNewLabel_1);
	}
}
