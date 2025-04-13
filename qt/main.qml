import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Script Output Viewer"

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Button {
            text: "Run Script"
            onClicked: tableModel.runScript()
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                model: tableModel
                delegate: Item {
                    width: ListView.view.width
                    height: 40

                    Text {
                        text: model.data // Display each line of output
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }
        }
    }
}
