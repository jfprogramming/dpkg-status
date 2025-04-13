#pragma once


#include <QAbstractTableModel>
#include <QProcess>

class DpkgModelData : public QAbstractTableModel {
    Q_OBJECT
public:
    explicit DpkgModelData(QObject *parent = nullptr);

    // Overridden methods for QAbstractTableModel
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Method to call the Python script
    Q_INVOKABLE void runScript();

private:
    QStringList m_data; // To store the output of the script
};
