#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QDebug>
#include <QFile>
#include <QDirIterator>
#include "dpkgmodeldata.h"

// un-comment to check system resources
//#define QT_DEBUG

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    // Register the DpkgModelData class with QML
    DpkgModelData tableModel;
    engine.rootContext()->setContextProperty("tableModel", &tableModel);


#ifdef QT_DEBUG
    QDirIterator it(":", QDirIterator::Subdirectories);
    while (it.hasNext()) {
        qDebug() << "Available Resource:" << it.next();
    }
#endif

    // Load QML file from the file system
    engine.load(QUrl(QStringLiteral("qrc:/dpkgstatus/qml/Main.qml")));
    if (engine.rootObjects().isEmpty()) {
        qCritical() << "Failed to load QML file.";
        return -1;
    }

    return app.exec();
}

