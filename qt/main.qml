import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "DPKG Status Script Output Viewer"
    color: "#f0f0f0" // Light background color for the whole window

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        // Header
        Rectangle {
            color: "#4CAF50" // Green header
            height: 50
            Layout.fillWidth: true

            Text {
                text: "DPKG Status Script Output Viewer"
                color: "white"
                font.pixelSize: 24
                font.bold: true
                anchors.centerIn: parent
            }
        }

        // Main Content Area
        Rectangle {
            color: "white"
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 8
            border.color: "#cccccc"
            border.width: 1
            anchors.margins: 10

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                // Styled Button
                Button {
                    text: "Run Script"
                    Layout.alignment: Qt.AlignHCenter
                    background: Rectangle {
                        color: "#4CAF50" // Green button background
                        radius: 8
                    }
                    contentItem: Text {
                        text: "Run Script"
                        color: "white"
                        font.pixelSize: 16
                        anchors.centerIn: parent
                    }
                    onClicked: tableModel.runScript()
                }

                // Scrollable ListView
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    background: Rectangle {
                        color: "#f9f9f9" // Light gray background for the scroll area
                        radius: 5
                    }

                    ListView {
                        model: tableModel
                        spacing: 5
                        delegate: Item {
                            width: ListView.view.width
                            height: 40

                            Rectangle {
                                width: parent.width
                                height: parent.height
                                color: index % 2 === 0 ? "#f5f5f5" : "#ffffff" // Alternating row colors
                                radius: 5
                                border.color: "#dddddd"
                                border.width: 1

                                Text {
                                    text: model.data // Display each line of output
                                    color: "#333333"
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.left: parent.left
                                    anchors.leftMargin: 10
                                    elide: Text.ElideRight
                                }
                            }
                        }
                    }
                }
            }
        }

        // Footer
        Rectangle {
            color: "#4CAF50" // Green footer
            height: 40
            Layout.fillWidth: true

            Text {
                text: "© 2025 DPKG Status Script Viewer App | Author: Jesse Finneman"
                color: "white"
                font.pixelSize: 14
                anchors.centerIn: parent
            }
        }
    }
}
