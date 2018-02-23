# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PACropRows
                                 A QGIS plugin
 This plugin generates crop rows lines from drone aerial images
                             -------------------
        begin                : 2018-02-22
        copyright            : (C) 2018 by Andres Herrera - Universidad del Valle
        email                : fabio.herrera@correounivalle.edu.co
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PACropRows class from file PACropRows.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .crop_rows import PACropRows
    return PACropRows(iface)
