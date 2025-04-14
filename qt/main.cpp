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

    // Connect to the warnings signal to log QML errors
    QObject::connect(&engine, &QQmlApplicationEngine::warnings, [](const QList<QQmlError> &warnings) {
        for (const auto &warning : warnings) {
            qCritical() << "QML Warning:" << warning.toString();
        }
    });

    // Register the DpkgModelData class with QML
    DpkgModelData tableModel;
    engine.rootContext()->setContextProperty("tableModel", &tableModel);

    qDebug() << "Resource Test:" << QUrl(QStringLiteral("qrc:/Main.qml")).isValid();
    qDebug() << "Resource Exists:" << QFile::exists(":/qml/Main.qml");
    // Load QML file from the file system
    engine.load(QUrl(QStringLiteral("qrc:/qt/qml/dpkgstatus/qml/Main.qml")));

    QDirIterator it(":", QDirIterator::Subdirectories);
    while (it.hasNext()) {
        qDebug() << "Available Resource:" << it.next();
    }

    if (engine.rootObjects().isEmpty()) {
        qCritical() << "Failed to load QML file.";
        return -1;
    }

    return app.exec();
}

