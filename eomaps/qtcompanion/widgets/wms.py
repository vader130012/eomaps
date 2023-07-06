from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStatusTipEvent

from ... import Maps, _data_dir
from pathlib import Path
import json
import os

# the path to which already fetched WebMap layers are stored
# (to avoid fetching available layers on menu-population)
wms_layers_dumppath = Path(_data_dir) / "_companion_wms_layers.json"


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


class WMSBase:
    def __init__(self):
        pass

    def ask_for_legend(self, wms, wmslayer):
        if hasattr(wms, "add_legend"):
            try:
                img = wms.fetch_legend(silent=True)
                if img is not None:
                    self._ask_for_legend(wms, wmslayer, img)
            except:
                pass

    def _ask_for_legend(self, wms, wmslayer, img=None):
        self._msg = QtWidgets.QMessageBox()
        self._msg.setIcon(QtWidgets.QMessageBox.Question)
        self._msg.setWindowTitle("Add a legend?")
        self._msg.setText(f"Do you want a legend for {wmslayer}?")
        self._msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self._msg.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        self._msg.buttonClicked.connect(lambda: self._cb_add_legend(wms, img))
        self._msg.show()

    def _cb_add_legend(self, wms, img):
        if self._msg.standardButton(self._msg.clickedButton()) != self._msg.Yes:
            return

        if hasattr(wms, "add_legend"):
            try:
                wms.add_legend(img=img)
            except:
                pass


class WMS_GEBCO(WMSBase):
    layer_prefix = "GEBCO_"
    name = "GEBCO"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = [
                key
                for key in self.m.add_wms.GEBCO.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for GEBCO", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.GEBCO.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_GMRT(WMSBase):
    layer_prefix = "GMRT_"
    name = "GMRT"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = [
                key
                for key in self.m.add_wms.GMRT.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for GMRT", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.GMRT.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_GLAD(WMSBase):
    layer_prefix = "GLAD_"
    name = "GLAD"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = [
                key
                for key in self.m.add_wms.GLAD.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for GLAD", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.GLAD.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_GOOGLE(WMSBase):
    layer_prefix = "GOOGLE_"
    name = "GOOGLE"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = [
                key
                for key in self.m.add_wms.GOOGLE.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for GOOGLE", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.GOOGLE.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_CAMS(WMSBase):
    layer_prefix = "CAMS_"
    name = "CAMS"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = [
                key
                for key in self.m.add_wms.CAMS.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for CAMS", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.CAMS.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_NASA_GIBS(WMSBase):
    layer_prefix = "NASA_GIBS_"
    name = "NASA_GIBS"

    def __init__(self, m=None):
        self.m = m

        if self.m.get_crs(3857) == m.crs_plot:
            self.usewms = self.m.add_wms.NASA_GIBS.EPSG_3857
        elif self.m.get_crs(3031) == m.crs_plot:
            self.usewms = self.m.add_wms.NASA_GIBS.EPSG_3031
        elif self.m.get_crs(3413) == m.crs_plot:
            self.usewms = self.m.add_wms.NASA_GIBS.EPSG_3413
        elif self.m.get_crs(4326) == m.crs_plot:
            self.usewms = self.m.add_wms.NASA_GIBS.EPSG_4326
        else:
            self.usewms = self.m.add_wms.NASA_GIBS.EPSG_3857

        try:
            self.wmslayers = [
                key
                for key in self.usewms.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for NASA_GIBS", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.usewms.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_Austria(WMSBase):
    layer_prefix = "AT_"
    name = "Austria"

    def __init__(self, m=None):
        self.m = m

        try:
            self._AT_layers = [
                "Austria__" + key
                for key in self.m.add_wms.Austria.AT_basemap.add_layer.__dict__
            ]
        except Exception as ex:
            self._AT_layers = []
            print("EOmaps: Problem while fetching wmslayers for AT_Austria", ex)

        try:
            self._Wien_layers = [
                "Wien__" + key
                for key in self.m.add_wms.Austria.Wien_basemap.add_layer.__dict__
            ]
        except Exception as ex:
            self._Wien_layers = []
            print("EOmaps: Problem while fetching wmslayers for AT_Wien", ex)

        self.wmslayers = [*self._AT_layers, *self._Wien_layers]

    def do_add_layer(self, wmslayer, layer):
        if wmslayer in self._AT_layers:
            wms = getattr(
                self.m.add_wms.Austria.AT_basemap.add_layer,
                remove_prefix(wmslayer, "Austria__"),
            )
        elif wmslayer in self._Wien_layers:
            wms = getattr(
                self.m.add_wms.Austria.Wien_basemap.add_layer,
                remove_prefix(wmslayer, "Wien__"),
            )

        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class ESRI_ArcGIS(WMSBase):
    layer_prefix = "ESRI"
    name = "ESRI_ArcGIS"

    def __init__(self, m=None):
        self.m = m

        self.m.add_wms.ESRI_ArcGIS

        self.wmslayers = []

        for servicename in self.m.add_wms.ESRI_ArcGIS._layers:
            self.wmslayers.extend(
                [
                    servicename + "__" + key
                    for key in getattr(
                        self.m.add_wms.ESRI_ArcGIS, servicename
                    ).__dict__.keys()
                    if not (key in ["m"] or key.startswith("_"))
                ]
            )

    def do_add_layer(self, wmslayer, layer):

        wms = None

        # check if we need to remove a prefix (e.g. from the dropdown-names)
        for servicename in self.m.add_wms.ESRI_ArcGIS._layers:
            prefix = f"{servicename}__"
            layers = [i for i in self.wmslayers if i.startswith(prefix)]
            if wmslayer in layers:
                service = getattr(self.m.add_wms.ESRI_ArcGIS, servicename, None)

                wms = getattr(
                    service, remove_prefix(wmslayer, prefix)
                ).add_layer.xyz_layer
                break

        if wms is None:
            print(f"EOaps: WebMap layer {wmslayer}, {layer} not found")
            return

        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_OSM(WMSBase):
    layer_prefix = "OSM_"
    name = "OpenStreetMap"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = [
                key
                for key in self.m.add_wms.OpenStreetMap.add_layer.__dict__.keys()
                if not (key in ["m"] or key.startswith("_"))
            ]
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for OSM", ex)

        try:
            self._terrestis = [
                "Terrestis__" + i
                for i in m.add_wms.OpenStreetMap.OSM_terrestis.add_layer.__dict__
            ]
        except Exception as ex:
            self._terrestis = []
            print("EOmaps: Problem while fetching wmslayers for OSM_terrestis", ex)

        try:
            self._mundialis = [
                "Mundialis__" + i
                for i in m.add_wms.OpenStreetMap.OSM_mundialis.add_layer.__dict__
            ]
        except Exception as ex:
            self._mundialis = []
            print("EOmaps: Problem while fetching wmslayers for OSM_mundialis", ex)

        try:
            self._OSM_landuse = [
                "OSM_landuse__" + i
                for i in m.add_wms.OpenStreetMap.OSM_landuse.add_layer.__dict__
            ]
        except Exception as ex:
            self._OSM_landuse = []
            print("Problem while fetching wmslayers for OSM_landuse", ex)

        try:
            self._OSM_wms = [
                "OSM_wms__" + i
                for i in m.add_wms.OpenStreetMap.OSM_wms.add_layer.__dict__
            ]
        except Exception as ex:
            self._OSM_wms = []
            print("Problem while fetching wmslayers for OSM_wms", ex)

        try:
            self._OSM_wheregroup = [
                "WhereGroup__" + i
                for i in m.add_wms.OpenStreetMap.OSM_wheregroup.add_layer.__dict__
            ]
        except Exception as ex:
            self._OSM_wheregroup = []
            print("Problem while fetching wmslayers for OSM_wheregroup", ex)

        try:
            self._OSM_waymarkedtrails = [
                "WaymarkedTrails__" + i
                for i in m.add_wms.OpenStreetMap.OSM_waymarkedtrails.add_layer.__dict__
            ]
        except Exception as ex:
            self._OSM_waymarkedtrails = []
            print("Problem while fetching wmslayers for OSM_waymarkedtrails", ex)

        try:
            self._OSM_openrailwaymap = [
                "OpenRailwayMap__" + i
                for i in m.add_wms.OpenStreetMap.OSM_openrailwaymap.add_layer.__dict__
            ]
        except Exception as ex:
            self._OSM_openrailwaymap = []
            print("Problem while fetching wmslayers for OSM_openrailwaymap", ex)

        try:
            self._OSM_cartodb = [
                "CartoDB__" + i
                for i in m.add_wms.OpenStreetMap.OSM_cartodb.add_layer.__dict__
            ]
        except Exception as ex:
            self._OSM_cartodb = []
            print("Problem while fetching wmslayers for OSM_cartodb", ex)

        self.wmslayers += self._terrestis
        self.wmslayers += self._mundialis
        self.wmslayers += self._OSM_landuse
        self.wmslayers += self._OSM_wms
        self.wmslayers += self._OSM_wheregroup
        self.wmslayers += self._OSM_waymarkedtrails
        self.wmslayers += self._OSM_openrailwaymap
        self.wmslayers += self._OSM_cartodb

    def do_add_layer(self, wmslayer, layer):

        wms = None

        # check if we need to remove a prefix (e.g. from the dropdown-names)
        for layers, servicename, prefix in (
            (self._OSM_wms, "OSM_wms", "OSM_wms__"),
            (self._OSM_landuse, "OSM_landuse", "OSM_landuse__"),
            (self._mundialis, "OSM_mundialis", "Mundialis__"),
            (self._terrestis, "OSM_terrestis", "Terrestis__"),
            (self._OSM_wheregroup, "OSM_wheregroup", "WhereGroup__"),
            (self._OSM_waymarkedtrails, "OSM_waymarkedtrails", "WaymarkedTrails__"),
            (self._OSM_openrailwaymap, "OSM_openrailwaymap", "OpenRailwayMap__"),
            (self._OSM_cartodb, "OSM_cartodb", "CartoDB__"),
        ):

            if wmslayer in layers:
                service = getattr(self.m.add_wms.OpenStreetMap, servicename, None)
                wms = getattr(service.add_layer, remove_prefix(wmslayer, prefix))
                break

        if wms is None:
            wms = getattr(self.m.add_wms.OpenStreetMap.add_layer, wmslayer)

        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_S2_cloudless(WMSBase):
    layer_prefix = "S2_"
    name = "S2 cloudless"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = sorted(self.m.add_wms.S2_cloudless.layers)
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for S2_cloudless", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.S2_cloudless.add_layer, wmslayer)
        wms(layer=layer)
        self.ask_for_legend(wms, wmslayer)


class WMS_ESA_WorldCover(WMSBase):
    layer_prefix = ""
    name = "ESA WorldCover"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = self.m.add_wms.ESA_WorldCover.layers
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for ESA_WorldCover", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.ESA_WorldCover.add_layer, wmslayer)
        wms(layer=layer)
        self.ask_for_legend(wms, wmslayer)


class WMS_S1GBM(WMSBase):
    layer_prefix = "S1GBM_"
    name = "S1GBM"

    def __init__(self, m=None):
        self.m = m
        self.wmslayers = ["vv", "vh"]

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.S1GBM.add_layer, wmslayer)
        wms(layer=layer)
        self.ask_for_legend(wms, wmslayer)


class WMS_ISRIC_SoilGrids(WMSBase):
    layer_prefix = "ISRIC_SG_"
    name = "ISRIC SoilGrids"

    def __init__(self, m=None):
        self.m = m

        subs = [i for i in m.add_wms.ISRIC_SoilGrids.__dir__() if not i.startswith("_")]

        self.wmslayers = []
        for l in subs:
            try:
                self.wmslayers.extend(
                    [
                        key
                        for key in getattr(
                            self.m.add_wms.ISRIC_SoilGrids, l
                        ).add_layer.__dict__.keys()
                        if not (key in ["m"] or key.startswith("_"))
                    ]
                )
            except Exception as ex:
                print(
                    "EOmaps: Problem while fetching wmslayers for ISRIC_SoilGrids "
                    f"{subs}",
                    ex,
                )

    def do_add_layer(self, wmslayer, layer):

        sub = wmslayer.split("_", 1)[0]

        wms = getattr(getattr(self.m.add_wms.ISRIC_SoilGrids, sub).add_layer, wmslayer)
        wms(layer=layer)
        self.ask_for_legend(wms, wmslayer)


class WMS_DLR_basemaps(WMSBase):
    layer_prefix = "DLR_bm_"
    name = "DLR basemaps"

    def __init__(self, m=None):
        self.m = m
        try:
            self.wmslayers = self.m.add_wms.DLR_basemaps.layers
        except Exception as ex:
            self.wmslayers = []
            print("EOmaps: Problem while fetching wmslayers for DLR_basemaps", ex)

    def do_add_layer(self, wmslayer, layer):
        wms = getattr(self.m.add_wms.DLR_basemaps.add_layer, wmslayer)
        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


class WMS_OpenPlanetary(WMSBase):
    layer_prefix = "OPM_"
    name = "OpenPlanetary"

    def __init__(self, m=None):
        self.m = m
        self.wmslayers = []

        try:
            self._moon = [
                "Moon__" + i
                for i in m.add_wms.OpenPlanetary.Moon.add_layer.__dict__
                if not i.startswith("_")
            ]
        except Exception as ex:
            self._moon = []
            print("EOmaps: Problem while fetching wmslayers for OpenPlanetary", ex)

        try:
            self._mars = [
                "Mars__" + i
                for i in m.add_wms.OpenPlanetary.Mars.add_layer.__dict__
                if not i.startswith("_")
            ]
        except Exception as ex:
            self._mars = []
            print("EOmaps: Problem while fetching wmslayers for OpenPlanetary", ex)

        self.wmslayers += self._moon
        self.wmslayers += self._mars

    def do_add_layer(self, wmslayer, layer):

        wms = None

        # check if we need to remove a prefix (e.g. from the dropdown-names)
        for layers, servicename, prefix in (
            (self._moon, "Moon", "Moon__"),
            (self._mars, "Mars", "Mars__"),
        ):

            if wmslayer in layers:
                service = getattr(self.m.add_wms.OpenPlanetary, servicename, None)
                wms = getattr(service.add_layer, remove_prefix(wmslayer, prefix))
                break

        if wms is None:
            print("EOmaps: the wms service {wmslayer} does not exist")
            return

        wms(layer=layer, transparent=True)
        self.ask_for_legend(wms, wmslayer)


# an event-filter to catch StatusTipFilter events
# (e.g. to avoid clearing the statusbar on mouse hoover over QMenu)
class StatusTipFilter(QObject):
    def eventFilter(self, watched, event):
        if isinstance(event, QStatusTipEvent):
            return True
        return super().eventFilter(watched, event)


class AddWMSMenuButton(QtWidgets.QPushButton):
    wmsLayerCreated = pyqtSignal(str)

    def __init__(self, *args, m=None, new_layer=False, show_layer=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.m = m
        self._new_layer = new_layer
        self._show_layer = show_layer
        self.layer = None

        self.wms_dict = {
            "OpenStreetMap": WMS_OSM,
            "S2 Cloudless": WMS_S2_cloudless,
            "ESA WorldCover": WMS_ESA_WorldCover,
            "S1GBM": WMS_S1GBM,
            "GEBCO": WMS_GEBCO,
            "GMRT": WMS_GMRT,
            "GLAD": WMS_GLAD,
            "GOOGLE": WMS_GOOGLE,
            "NASA GIBS": WMS_NASA_GIBS,
            "CAMS": WMS_CAMS,
            "ISRIC SoilGrids": WMS_ISRIC_SoilGrids,
            "DLR Basemaps": WMS_DLR_basemaps,
            "ESRI_ArcGIS": ESRI_ArcGIS,
            "Austria Basemaps": WMS_Austria,
            "OpenPlanetary": WMS_OpenPlanetary,
        }

        if self._new_layer:
            self.setText("Create new WebMap Layer")
        else:
            self.setText("Add WebMap Service")

        width = self.fontMetrics().boundingRect(self.text()).width()
        self.setFixedWidth(width + 30)

        self.feature_menu = QtWidgets.QMenu()
        self.feature_menu.setStyleSheet("QMenu { menu-scrollable: 1;}")
        self.feature_menu.aboutToShow.connect(self.populate_menu)

        self.setMenu(self.feature_menu)
        self.clicked.connect(self.show_menu)

        # try to fetch cached wms-layer names (to populate dropdown)
        # The cache will be updated if a layer of the wms-service is added to the map!
        # (since then the layers are anyways re-fetched)
        if wms_layers_dumppath.exists():
            try:
                with open(wms_layers_dumppath, "r") as file:
                    self._submenus = json.load(file)
            except Exception:
                print(
                    "EOmaps: Unable to load cached wms-layers from:\n    ",
                    wms_layers_dumppath,
                )
                self._submenus = dict()
        else:
            self._submenus = dict()

        # set event-filter to avoid showing tooltips on hovver over QMenu items
        self.installEventFilter(StatusTipFilter(self))

    def enterEvent(self, e):
        if self.window().showhelp is True:
            if self._new_layer:
                QtWidgets.QToolTip.showText(
                    e.globalPos(),
                    "<h3>New WebMap Layer</h3>"
                    "Create a new layer (<i>''[wms service]_[wms layer]''</i>) and add "
                    "the selected WebMap service to it."
                    "<p>"
                    "NOTE: The service is added to a new layer, <not> the "
                    "currently visible layer! (this is particularly useful to compare "
                    "existing layers to WebMap layers)",
                )
            else:
                QtWidgets.QToolTip.showText(
                    e.globalPos(),
                    "<h3>Add WebMap Service</h3>"
                    "Add the selected WebMap service to the "
                    "<b>currently selected layer-tab</b> "
                    "in the tab-bar below."
                    "<p>"
                    "NOTE: This is not necessarily the currently visible layer!",
                )

    @pyqtSlot()
    def show_menu(self):
        self.feature_menu.popup(self.mapToGlobal(self.menu_button.pos()))

    @pyqtSlot()
    def populate_menu(self):

        self.sub_menus = dict()
        for wmsname in self.wms_dict:
            self.sub_menus[wmsname] = self.feature_menu.addMenu(wmsname)
            self.sub_menus[wmsname].aboutToShow.connect(self._populate_submenu_cb)
        self.feature_menu.aboutToShow.disconnect()

    @pyqtSlot()
    def _populate_submenu_cb(self):
        wmsname = self.sender().title()
        self.fetch_submenu(wmsname=wmsname)
        self.populate_submenu(wmsname)

    def select_wmslayers(self, wmsname, wmslayers):
        """
        Pre-select WMS-layers of services based on certain conditions
        (e.g. to avoid showing layers that cannot be plottet)

        Parameters
        ----------
        wmsname : str
            the name of the wms.
        wmslayers : list
            the list of ALL available layers

        Returns
        -------
        list
            a list of the selected layers.

        """
        if wmsname == "S2 Cloudless":
            if self.m.crs_plot == self.m.CRS.GOOGLE_MERCATOR:
                wmslayers = [i for i in wmslayers if i.endswith("3857")]
            else:
                wmslayers = [i for i in wmslayers if not i.endswith("3857")]
        elif wmsname == "ESA WorldCover":
            wmslayers = [
                key
                for key in wmslayers
                if (key.startswith("WORLDCOVER") or key.startswith("COP"))
            ]

        return wmslayers

    def set_layer(self, layer):
        self.layer = layer

    def fetch_submenu(self, wmsname):
        try:
            # disconnect callbacks to avoid recursions
            self.sub_menus[wmsname].aboutToShow.disconnect()

            self._fetch_submenu(wmsname)
        except Exception as ex:
            print(f"EOmaps: problem while trying to fetch the submenu for {wmsname}")

    def _fetch_submenu(self, wmsname):
        if wmsname in getattr(Maps, "_companion_wms_submenus", dict()):
            self._submenus[wmsname] = Maps._companion_wms_submenus[wmsname]

        if wmsname in self._submenus:
            return

        print(f"EOmaps: Fetching WMS layers for {wmsname} ...")

        wmsclass = self.wms_dict[wmsname]
        wms = wmsclass(m=self.m)
        sub_features = wms.wmslayers
        self._submenus[wmsname] = sub_features

        if not hasattr(Maps, "_companion_wms_submenus"):
            Maps._companion_wms_submenus = dict()
        Maps._companion_wms_submenus[wmsname] = sub_features

        self._update_layer_cache(wmsname, wms.wmslayers)

    def populate_submenu(self, wmsname=None):
        if wmsname not in self._submenus:
            print("No layers found for the WMS: {wmsname}")
            return
        else:
            sub_features = self.select_wmslayers(wmsname, self._submenus[wmsname])

        try:
            submenu = self.sub_menus[wmsname]

            for wmslayer in sub_features:
                action = submenu.addAction(wmslayer)
                action.triggered.connect(self.menu_callback_factory(wmsname, wmslayer))

        except Exception:
            print("There was a problem with the WMS: " + wmsname)

    @pyqtSlot()
    def menu_callback_factory(self, wmsname, wmslayer):
        @pyqtSlot()
        def wms_cb():
            wmsclass = self.wms_dict[wmsname]
            wms = wmsclass(m=self.m)

            if self._new_layer:
                layer = wms.layer_prefix + wmslayer
                # indicate creation of new layer in statusbar
                self.window().statusBar().showMessage(
                    f"New WebMap layer '{layer}' created!", 5000
                )

            else:
                layer = self.layer
                if layer.startswith("_") and "|" in layer:
                    self.window().statusBar().showMessage(
                        "Adding features to temporary multi-layers is not supported!",
                        5000,
                    )
                    return

            wms.do_add_layer(wmslayer, layer=layer)

            # update the cached layer-names if necessary
            self._update_layer_cache(wmsname, wms.wmslayers)

            # emit a signal that a new layer has been created
            self.wmsLayerCreated.emit(str(layer))

            if self._show_layer:
                self.m.show_layer(layer)

            # call draw to make sure the wms service is properly fetched
            self.m.BM.canvas.draw_idle()

        return wms_cb

    def _update_layer_cache(self, wmsname, layers):
        """
        Update the layer-cache for the wms-menu-buttons

        The cache is located at:

        >>> from eomaps import _data_dir
        >>> print(_data_dir)

        Parameters
        ----------
        wmsname : str
            the name of the wms-service.
        layers : list
            a list of layer-names.
        """

        # make sure the cache-directory has been initialized
        if not os.path.isdir(_data_dir):
            os.makedirs(_data_dir)

        try:
            if wms_layers_dumppath.exists():
                with open(wms_layers_dumppath, "r") as file:
                    cache = json.load(file)
            else:
                cache = dict()

            if wmsname in cache:
                # if new layers are found, update the cache for this service!
                if set(cache[wmsname]) != set(layers):
                    update = True
                else:
                    update = False
            else:
                update = True

            if update:
                cache[wmsname] = layers
                with open(wms_layers_dumppath, "w") as file:
                    json.dump(cache, file)

        except Exception:
            from warnings import warn

            warn(
                "EOmaps: PROBLEM while trying to save fetched WMS layers to:\n"
                f"{wms_layers_dumppath}"
            )
            pass

    @classmethod
    def fetch_all_wms_layers(cls, m, refetch=False):
        """
        A convenience function to fetch (and cache) all available WMS-layers
        for the companion-widget

        Parameters
        ----------
        m : eomaps.Maps
            The Maps-object to use.
        refetch : bool, optional

        - If True, ALL layers will be re-fetched.
        - If False, the cached layers are loaded and returned as dict

        The default is False.

        Returns
        -------
        dict
            The cached webmap layer names.

        """
        print("EOmaps: Fetching WMS layers for the companion widget...")

        b = cls(m=m)

        if refetch is True:
            b._submenus = dict()

        for wmsname in b.wms_dict:
            b._fetch_submenu(wmsname)

        return b._submenus
