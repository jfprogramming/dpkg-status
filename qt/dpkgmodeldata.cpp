#include "dpkgmodeldata.h"
#include <QDebug>

DpkgModelData::DpkgModelData(QObject *parent): QAbstractTableModel(parent)
{
}

int DpkgModelData::rowCount(const QModelIndex &parent) const {
    Q_UNUSED(parent);
    return m_data.size(); // Each line of output is a row
}

int DpkgModelData::columnCount(const QModelIndex &parent) const {
    Q_UNUSED(parent);
    return 1; // Single column showing script output
}

QVariant DpkgModelData::data(const QModelIndex &index, int role) const {
    if (!index.isValid() || role != Qt::DisplayRole)
        return QVariant();

    return m_data.at(index.row());
}

void DpkgModelData::runScript() {
    QProcess process;
    process.start("dpkg-status.py"); // Call the installed Python script
    if (!process.waitForFinished()) {
        QString errorOutput = process.readAllStandardError();
        qWarning() << "Failed to run script: " << process.errorString();
        qWarning() << "Standard error output: " << errorOutput;
    }

    // Notify the view that the data is about to change
    beginResetModel();

    // Capture output and split into lines
    QString output = process.readAllStandardOutput();
    m_data = output.split('\n', Qt::SkipEmptyParts);

    // Notify the view that the data has changed
    endResetModel();
}
