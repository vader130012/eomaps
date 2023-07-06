from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSlot

from .utils import EditLayoutButton


class DpiInput(QtWidgets.QLineEdit):
    def enterEvent(self, e):
        if self.window().showhelp is True:
            QtWidgets.QToolTip.showText(
                e.globalPos(),
                "<h3>Output DPI</h3>" "Set the DPI used for exporting png images.",
            )


class TransparentCheckBox(QtWidgets.QCheckBox):
    def enterEvent(self, e):
        if self.window().showhelp is True:
            QtWidgets.QToolTip.showText(
                e.globalPos(),
                "<h3>Frame transparency</h3>"
                "Toggle the transparency of the axis-frame."
                "<p>"
                "If checked, the map will be exported with a transparent background.",
            )


class TightBboxCheckBox(QtWidgets.QCheckBox):
    def enterEvent(self, e):
        if self.window().showhelp is True:
            QtWidgets.QToolTip.showText(
                e.globalPos(),
                "<h3>Export figure with a tight bbox</h3>"
                "If checked, The exported figure will use the smallest "
                "bounding-box that contains all artists. "
                "The input-box can be used to add a padding (in inches) on all sides.",
            )


class TightBboxInput(QtWidgets.QLineEdit):
    def enterEvent(self, e):
        if self.window().showhelp is True:
            QtWidgets.QToolTip.showText(
                e.globalPos(),
                "<h3>Tight Bbox padding</h3>"
                "Set the padding (in inches) that is added to each side of the "
                "figure when exporting it with a tight bounding-box",
            )


class RefetchWMSCheckBox(QtWidgets.QCheckBox):
    def enterEvent(self, e):
        if self.window().showhelp is True:
            QtWidgets.QToolTip.showText(
                e.globalPos(),
                "<h3>Frame transparency</h3>"
                "Toggle re-fetching WebMap services on figure-export."
                "<p>"
                "If checked, all WebMap services will be re-fetched with respect to "
                "the export-dpi before saving the figure. "
                "<p>"
                "NOTE: For high dpi-exports, this can result in a very large number of "
                "tiles that need to be fetched from the server. "
                "If the request is too large, the server might refuse it and the final "
                "image can have gaps (or no wms-tiles at all)!",
            )


class SaveButton(QtWidgets.QPushButton):
    def enterEvent(self, e):
        if self.window().showhelp is True:
            QtWidgets.QToolTip.showText(
                e.globalPos(),
                "<h3>Save the figure</h3>"
                "Open a file-dialog to save the figure."
                "<p>"
                "The specified file-ending will be used to determine the export-type!",
            )


class SaveFileWidget(QtWidgets.QFrame):
    def __init__(self, *args, m=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.m = m

        b_edit = EditLayoutButton("Edit layout", m=self.m)
        width = b_edit.fontMetrics().boundingRect(b_edit.text()).width()
        b_edit.setFixedWidth(width + 30)

        b1 = SaveButton("Save!")
        width = b1.fontMetrics().boundingRect(b1.text()).width()
        b1.setFixedWidth(width + 30)

        b1.clicked.connect(self.save_file)

        # dpi
        l1 = QtWidgets.QLabel("DPI:")
        width = l1.fontMetrics().boundingRect(l1.text()).width()
        l1.setFixedWidth(width + 5)

        self.dpi_input = DpiInput()
        self.dpi_input.setMaximumWidth(50)
        validator = QtGui.QIntValidator()
        self.dpi_input.setValidator(validator)
        self.dpi_input.setText("100")

        # transparent
        self.transp_cb = TransparentCheckBox()
        transp_label = QtWidgets.QLabel("Tranparent")
        width = transp_label.fontMetrics().boundingRect(transp_label.text()).width()
        transp_label.setFixedWidth(width + 5)

        # refetch WebMap services
        self.refetch_cb = RefetchWMSCheckBox()
        refetch_label = QtWidgets.QLabel("Re-fetch WebMaps")
        width = transp_label.fontMetrics().boundingRect(refetch_label.text()).width()
        refetch_label.setFixedWidth(width + 5)

        # tight bbox
        self.tightbbox_cb = TightBboxCheckBox()
        tightbbox_label = QtWidgets.QLabel("Tight Bbox")
        width = (
            tightbbox_label.fontMetrics().boundingRect(tightbbox_label.text()).width()
        )
        tightbbox_label.setFixedWidth(width + 5)

        self.tightbbox_input = TightBboxInput()
        self.tightbbox_input.setMaximumWidth(50)
        validator = QtGui.QDoubleValidator()
        self.tightbbox_input.setValidator(validator)
        self.tightbbox_input.setText("0.1")
        self.tightbbox_input.setVisible(False)

        self.tightbbox_cb.stateChanged.connect(self.tight_cb_callback)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(b_edit)
        layout.addStretch(1)
        layout.addWidget(l1)
        layout.addWidget(self.dpi_input)
        layout.addWidget(transp_label)
        layout.addWidget(self.transp_cb)
        layout.addWidget(refetch_label)
        layout.addWidget(self.refetch_cb)

        layout.addWidget(tightbbox_label)
        layout.addWidget(self.tightbbox_cb)
        layout.addWidget(self.tightbbox_input)

        layout.addWidget(b1)

        layout.setAlignment(Qt.AlignBottom)

        self.setLayout(layout)
        self.setStyleSheet(
            """
            SaveFileWidget{
                border: 1px solid rgb(200,200,200);
                border-radius: 10px;
                };
            """
        )

    @pyqtSlot()
    def tight_cb_callback(self):
        if self.tightbbox_cb.isChecked():  # e.g. checked
            self.tightbbox_input.setVisible(True)
        else:
            self.tightbbox_input.setVisible(False)

    @pyqtSlot()
    def save_file(self):
        savepath = QtWidgets.QFileDialog.getSaveFileName()[0]
        if savepath is not None and savepath != "":

            kwargs = dict()
            if self.tightbbox_cb.isChecked():
                kwargs["bbox_inches"] = "tight"
                kwargs["pad_inches"] = float(self.tightbbox_input.text())

            self.m.savefig(
                savepath,
                dpi=int(self.dpi_input.text()),
                transparent=self.transp_cb.isChecked(),
                refetch_wms=self.refetch_cb.isChecked(),
                **kwargs
            )
