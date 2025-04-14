#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QDebug>
#include <QFile>
#include <QDirIterator>
#include "dpkgmodeldata.h"


int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    // Register the DpkgModelData class with QML
    DpkgModelData tableModel;
    engine.rootContext()->setContextProperty("tableModel", &tableModel);

    // Load QML file from the file system
    engine.load(QUrl(QStringLiteral("qrc:/qt/qml/dpkgstatus/qml/Main.qml")));
    if (engine.rootObjects().isEmpty()) {
        qCritical() << "Failed to load QML file.";
        return -1;
    }

    return app.exec();
}

