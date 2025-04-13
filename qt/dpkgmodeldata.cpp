#include "dpkgmodeldata.h"
#include <QProcess>
#include <QDebug>

DpkgModelData::DpkgModelData(QObject *parent)
    : QAbstractListModel(parent)
{
}

int DpkgModelData::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid())
        return 0;
    return m_data.size();
}

QVariant DpkgModelData::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || role != Qt::DisplayRole)
        return QVariant();

    return m_data.at(index.row());
}

QHash<int, QByteArray> DpkgModelData::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[Qt::DisplayRole] = "data"; // The "data" role will be used in QML
    return roles;
}

void DpkgModelData::runScript()
{
    QProcess process;
    // Run the Python script installed in the system by the custom deb package
    process.start("dpkg_status.py");

    if (!process.waitForFinished()) {
        qWarning() << "Failed to run script:" << process.errorString();
        return;
    }

    QString output = process.readAllStandardOutput();
    QStringList lines = output.split("\n");

    beginResetModel();
    m_data = lines; // Update the model with the script output
    endResetModel();
}
