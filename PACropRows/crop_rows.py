# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PACropRows
                                 A QGIS plugin
 This plugin generates crop rows lines from drone aerial images
                              -------------------
        begin                : 2018-02-22
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Andres Herrera - Universidad del Valle
        email                : fabio.herrera@correounivalle.edu.co
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import *
from qgis.gui import *
#from qgis.core import QgsMapLayer, QgsMapLayerRegistry
#from qgis.gui import QgsMapLayerComboBox, QgsMapLayerProxyModel, QgsFieldComboBox


# Initialize Qt resources from file resources.py
import resources
import resources_icons
# Import the code for the dialog
from crop_rows_dialog import PACropRowsDialog
import os.path


class PACropRows:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PACropRows_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Crop Rows Generator')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PACropRows')
        self.toolbar.setObjectName(u'PACropRows')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PACropRows', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = PACropRowsDialog()
        icon_path = ':/plugins/PACropRows/icon.png'
		
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PACropRows/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Crop Rows Toolbox'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Crop Rows Generator'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""

        ## Load layers and add to comboboxes
        #layers = self.iface.legendInterface().layers()
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        #Clear combobox 
        self.dlg.vectormask_Box.clear()
        self.dlg.rastermosaic_Box.clear()
        #layer_list = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and (layer.wkbType()==QGis.WKBPolygon or layer.wkbType() == QGis.WKBMultiPolygon):
                self.dlg.vectormask_Box.addItem(layer.name(), layer)
            if layer.type() == QgsMapLayer.RasterLayer:
                self.dlg.rastermosaic_Box.addItem(layer.name(), layer)
            #layer_list.append(layer.name())
        #self.dlg.vectormask_Box.addItems(layer_list)

        self.dlg.aboutTextBrowser.append("<span>This plugin is part of a master thesis of <b>AN AUTOMATIC CROP ROWS GENERATOR USING AERIAL HIGH-RESOLUTION IMAGES FOR PRECISION AGRICULTURE</b></span>")
        self.dlg.aboutTextBrowser.append("<span>in partial fulfillment of the requirements for the degree of:</span>")
        self.dlg.aboutTextBrowser.append("<span>Magister en Ingenier&iacute;a con &Eacute;nfasis en Ingenier&iacute;a de Sistemas y Computaci&oacute;n</span>")
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass