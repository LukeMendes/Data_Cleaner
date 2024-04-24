import os
from pathlib import Path
os.chdir(Path(__file__).parent)
import pandas
import numpy
from ydata_profiling import ProfileReport

class DataCleaner:
    def __init__(self, csv):
        """legt ein Objekt der Klasse "DataCleaner" an"""
        self.__alte_csv = self.__datei_einlesen(csv)
        self.__neue_csv = self.__datei_einlesen(csv)
        self.__NULL = None
        self.__redundante_header = None
        self.__duplikate = None
    def __datei_einlesen(self, csv):
        """liest die gewünschte CSV-Datei beim Initialisieren an, geschieht automatisch beim Anlegen des Objekts"""
        return pandas.read_csv(csv)

    def NULL_filtern(self):
        """ermöglicht das Anzeigen leerer Reihen mit "get_NULL()" (zeigt diese selbst nicht) und
        entfernt alle Reihen mit leeren Werten und legt den Rest in einer neuen Version ab"""
        self.__NULL = self.__neue_csv.isnull()
        self.__NULL = self.__NULL.replace(False, numpy.nan)
        self.__NULL = self.__NULL.dropna(how='all', subset=["Order ID", "Product", "Quantity Ordered",
                                                            "Price Each", "Order Date", "Purchase Address"])
        self.__NULL = self.__NULL
        self.__neue_csv = self.__neue_csv.dropna(how="all")
    def redundante_header_filtern(self):
        """ermöglicht das Anzeigen redundanter Header mit "get_redundante_header()" (zeigt diese selbst nicht) und
        entfernt alle redundanten Header und legt den Rest in einer neuen Version ab"""
        self.__redundante_header = self.__neue_csv[self.__neue_csv.eq(self.__neue_csv.columns).any(axis=1)]
        self.__neue_csv = self.__neue_csv[self.__neue_csv.ne(self.__neue_csv.columns).any(axis=1)]
    def duplikate_filtern(self):
        """ermöglicht das Anzeigen doppelter Reihen mit "get_duplikate()" (zeigt diese selbst nicht) und
        entfernt alle doppelten Reihen und legt den Rest in einer neuen Version ab"""
        self.__duplikate = self.__neue_csv[self.__neue_csv.duplicated(keep="first")]
        self.__neue_csv = self.__neue_csv.drop_duplicates(keep="first", subset=["Order ID", "Product",
                                                                                "Quantity Ordered", "Price Each",
                                                                                "Order Date", "Purchase Address"])

    def spalten_überarbeiten(self):
        """überarbeitet Spalten, die Strings enthalten so, dass alles in Großbuchstaben geschrieben ist und Leerzeichen
        durch "_" ersetzt werden und legt das Ergebnis in einer neuen Version ab"""
        self.__neue_csv["Product"] = self.__neue_csv["Product"].str.upper().str.replace(" ", "_")
        self.__neue_csv["Purchase Address"] = self.__neue_csv["Purchase Address"].str.upper().str.replace(" ", "_")
    def header_überarbeiten(self):
        """überarbeitet den Header so, dass alles in Großbuchstaben geschrieben ist und Leerzeichen durch "_" ersetzt
        werden und legt das Ergebnis in einer neuen Version ab"""
        self.__neue_csv.columns = self.__neue_csv.columns.str.upper().str.replace(" ", "_")

    def report_erstellen(self):
        """erstellt den Report für die originale und die bereinigte Version (ist nur dann wirklich bereinigt,
        wenn vorher alle leeren Werte, redundante Header und doppelten Reihen gefiltert wurden)"""
        profile_alt = ProfileReport(self.__alte_csv)
        profile_alt.to_file(output_file="./profiles/input_file.html")
        profile_neu = ProfileReport(self.__neue_csv)
        profile_neu.to_file(output_file="./profiles/output_file.html")
    def csv_erstellen(self):
        """erstellt eine CSV-Datei die, der bereinigten Version der Daten, die eingelesen wurden, entspricht"""
        self.__neue_csv.to_csv("./data/my_data_clean.csv")

    def get_NULL(self):
        """zeigt die Reihen an, die im Original leere Werte enthalten (muss vorher gefiltert werden)"""
        if self.__NULL is None:
            return "Es wurden noch keine NULL-Werte gefiltert."
        else:
            return self.__NULL
    def get_redundante_header(self):
        """zeigt die Reihen an, die im Original redundante Header sind (muss vorher gefiltert werden)"""
        if self.__redundante_header is None:
            return "Es wurden noch keine redundanten Header gefiltert."
        else:
            return self.__redundante_header
    def get_duplikate(self):
        """zeigt die Reihen an, die im Original doppelt sind (muss vorher gefiltert werden)"""
        if self.__duplikate is None:
            return "Es wurden noch keine doppelten Werte gefiltert."
        else:
            return self.__duplikate

def main():
    """Startet das Programm, wenn diese Datei für Tests ausgeführt wird"""
    tabelle = DataCleaner("./my_data.csv")
    tabelle.NULL_filtern()
    tabelle.redundante_header_filtern()
    tabelle.duplikate_filtern()
    tabelle.spalten_überarbeiten()
    tabelle.header_überarbeiten()
    tabelle.report_erstellen()
    tabelle.csv_erstellen()


if __name__ == "__main__": # nur in dieser Datei True
    main()