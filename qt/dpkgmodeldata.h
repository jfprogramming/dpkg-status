#pragma once

#include <QAbstractTableModel>
#include <QProcess>

class DpkgModelData : public QAbstractListModel
{
    Q_OBJECT

public:
    explicit DpkgModelData(QObject *parent = nullptr);

    // Override rowCount to return the number of rows
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    // Override data to return the data for each role
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Expose the role names to QML
    QHash<int, QByteArray> roleNames() const override;

    // Method to populate the model with script output
    Q_INVOKABLE void runScript();

private:
    QStringList m_data; // Store script output lines
};

