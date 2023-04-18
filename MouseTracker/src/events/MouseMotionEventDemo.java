/*
 * Copyright (c) 1995, 2008, Oracle and/or its affiliates. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   - Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 *   - Neither the name of Oracle or the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */ 

package events;

/*
 * MouseMotionEventDemo.java
 *
 */

import java.awt.*;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;

import javax.swing.*;

public class MouseMotionEventDemo extends JPanel
        implements MouseMotionListener, MouseListener {

    JPanel image;
//    BlankArea blankArea;
    JTextArea textArea;

    static boolean tracking = false;
    static boolean hasTracked = false;
    static int mousePosX = -1;
    static int mousePosY = -1;

    static final String NEWLINE = System.getProperty("line.separator");
    
    public static void main(String[] args) {
        /* Use an appropriate Look and Feel */
        try {
//            UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
//            UIManager.setLookAndFeel("com.sun.java.swing.plaf.gtk.GTKLookAndFeel");
            UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
        } catch (UnsupportedLookAndFeelException | ClassNotFoundException | InstantiationException | IllegalAccessException ex) {
            ex.printStackTrace();
        }
        /* Turn off metal's use of bold fonts */
        UIManager.put("swing.boldMetal", Boolean.FALSE);
        //Schedule a job for the event dispatch thread:
        //creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {

            long avgDelta = 0;
            long steps = 0;

            public void run() {

                //Create and set up the window.
                JFrame frame = new JFrame("Circuit Mouse Tracker");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

                //Create and set up the content pane.
                JComponent newContentPane = new MouseMotionEventDemo();
                newContentPane.setOpaque(true); //content panes must be opaque
                frame.setContentPane(newContentPane);

                //Display the window.
                frame.pack();
                frame.setVisible(true);


                new Thread(() -> {
                    while(true) {

                        long startT = System.currentTimeMillis();

                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }

                        synchronized (this){
                            if(tracking) {
                                System.out.println(mousePosX + ", " + mousePosY);
                                avgDelta+= System.currentTimeMillis() - startT;
                                ++steps;
                            } else if(hasTracked) {
                                avgDelta = avgDelta / steps;
                                System.out.println("Avg delta: " + avgDelta);
                                steps = 0;
                                avgDelta = 0;
                                hasTracked = false;
                            }
                        }
                    }
                }).start();


            }
        });
    }

    public MouseMotionEventDemo() {
        super(new GridLayout(0,1));
        image = new ImagePanel("big_circuit.jpeg");
//        blankArea = new BlankArea(Color.YELLOW);
        add(image);
//        add(blankArea);
        
        textArea = new JTextArea();
        textArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(textArea,
                JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
                JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setPreferredSize(new Dimension(200, 75));
        
        add(scrollPane);
        
        //Register for mouse events on blankArea and panel.
//        blankArea.addMouseMotionListener(this);
        image.addMouseMotionListener(this);
        addMouseMotionListener(this);
//        blankArea.addMouseListener(this);
        image.addMouseListener(this);
        addMouseListener(this);

        setPreferredSize(new Dimension(450, 450));
        setBorder(BorderFactory.createEmptyBorder(20,20,20,20));
    }
    
    void eventOutput(MouseEvent e) {

        if(e.getClickCount() > 0) {
            if (tracking) {
                textArea.append(
                        "Starting tracking @ (" + e.getX() + ", " + e.getY() + ")"
                                + NEWLINE);

            } else {
                textArea.append(
                        "Ending tracking @ (" + e.getX() + ", " + e.getY() + ")"
                                + NEWLINE);
                hasTracked = true;
            }
        } else {

            mousePosX = e.getX();
            mousePosY = e.getY();

            textArea.append(
                    "(" + e.getX() + "," + e.getY() + ")"
                            + NEWLINE);
            textArea.setCaretPosition(textArea.getDocument().getLength());
        }

    }

    
    public void mouseMoved(MouseEvent e) {
        synchronized (this) {
            if(tracking) eventOutput(e);
        }
    }
    
    public void mouseDragged(MouseEvent e) {
        //eventOutput("Mouse dragged", e);
    }

    public void mouseClicked(MouseEvent e) {
        synchronized (this) {
            tracking = !tracking;
            eventOutput(e);
        }
    }

    @Override
    public void mousePressed(MouseEvent e) {

    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }
}
