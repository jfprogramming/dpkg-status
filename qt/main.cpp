#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "dpkgmodeldata.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    // Register the DpkgModelData class with QML
    DpkgModelData tableModel;
    engine.rootContext()->setContextProperty("tableModel", &tableModel);

    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
