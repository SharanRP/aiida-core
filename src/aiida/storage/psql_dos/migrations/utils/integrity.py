###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Methods to validate the database integrity and fix violations."""
from __future__ import annotations

from aiida.common.log import AIIDA_LOGGER

LOGGER = AIIDA_LOGGER.getChild(__file__)

WARNING_BORDER = '*' * 120

# These are all the entry points from the `aiida.calculations` category as registered with the AiiDA registry
# on Tuesday December 4 at 13:00:00 UTC
registered_calculation_entry_points = [
    'ase.ase = aiida_ase.calculations.ase:AseCalculation',
    'castep.bs = aiida_castep.calculations.castep:CastepBSCalculation',
    'castep.castep = aiida_castep.calculations.castep:CastepCalculation',
    'castep.pot1d = aiida_castep.calculations.castep:Pot1dCalculation',
    'castep.spec = aiida_castep.calculations.castep:CastepSpectralCalculation',
    'castep.ts = aiida_castep.calculations.castep:CastepTSCalculation',
    'codtools.cifcellcontents = aiida_codtools.calculations.cifcellcontents:CifcellcontentsCalculation',
    'codtools.cifcodcheck = aiida_codtools.calculations.cifcodcheck:CifcodcheckCalculation',
    'codtools.cifcoddeposit = aiida_codtools.calculations.cifcoddeposit:CifcoddepositCalculation',
    'codtools.cifcodnumbers = aiida_codtools.calculations.cifcodnumbers:CifcodnumbersCalculation',
    'codtools.ciffilter = aiida_codtools.calculations.ciffilter:CiffilterCalculation',
    'codtools.cifsplitprimitive = aiida_codtools.calculations.cifsplitprimitive:CifsplitprimitiveCalculation',
    'cp2k = aiida_cp2k.calculations:Cp2kCalculation',
    'crystal17.basic = aiida_crystal17.calculations.cry_basic:CryBasicCalculation',
    'crystal17.immigrant = aiida_crystal17.calculations.cry_main_immigrant:CryMainImmigrantCalculation',
    'crystal17.main = aiida_crystal17.calculations.cry_main:CryMainCalculation',
    'ddec = aiida_ddec.calculations:DdecCalculation',
    'diff = aiida_diff.calculations:DiffCalculation',
    'dynaphopy = aiida_lammps.calculations.dynaphopy: DynaphopyCalculation',
    'gollum.gollum = aiida_gollum.calculations.gollum:GollumCalculation',
    'gudhi.rdm = aiida_gudhi.calculations.rips:RipsDistanceMatrixCalculation',
    'kkr.kkr = aiida_kkr.calculations.kkr:KkrCalculation',
    'kkr.kkrimp = aiida_kkr.calculations.kkrimp:KkrimpCalculation',
    'kkr.kkrimporter = aiida_kkr.calculations.kkrimporter:KkrImporterCalculation',
    'kkr.voro = aiida_kkr.calculations.voro:VoronoiCalculation',
    'lammps.combinate = aiida_lammps.calculations.lammps.combinate:CombinateCalculation',
    'lammps.force = aiida_lammps.calculations.lammps.force:ForceCalculation',
    'lammps.md = aiida_lammps.calculations.lammps.md:MdCalculation',
    'lammps.optimize = aiida_lammps.calculations.lammps.optimize:OptimizeCalculation',
    'nwchem.basic = aiida_nwchem.calculations.basic:BasicCalculation',
    'nwchem.pymatgen = aiida_nwchem.calculations.nwcpymatgen:NwcpymatgenCalculation',
    'phonopy.phono3py = aiida_phonopy.calculations.phonopy.phono3py: Phono3pyCalculation',
    'phonopy.phonopy = aiida_phonopy.calculations.phonopy.phonopy: PhonopyCalculation',
    'phtools.dmatrix = aiida_phtools.calculations.distance_matrix:DistanceMatrixCalculation',
    'phtools.surface = aiida_phtools.calculations.pore_surface:PoreSurfaceCalculation',
    'qeq.eqeq = aiida_qeq.calculations.eqeq:EQeqCalculation',
    'qeq.qeq = aiida_qeq.calculations.qeq:QeqCalculation',
    'quantumespresso.cp = aiida_quantumespresso.calculations.cp:CpCalculation',
    'quantumespresso.dos = aiida_quantumespresso.calculations.dos:DosCalculation',
    'quantumespresso.hp = aiida_quantumespresso_hp.calculations.hp:HpCalculation',
    'quantumespresso.matdyn = aiida_quantumespresso.calculations.matdyn:MatdynCalculation',
    'quantumespresso.namelists = aiida_quantumespresso.calculations.namelists:NamelistsCalculation',
    'quantumespresso.neb = aiida_quantumespresso.calculations.neb:NebCalculation',
    'quantumespresso.ph = aiida_quantumespresso.calculations.ph:PhCalculation',
    'quantumespresso.pp = aiida_quantumespresso.calculations.pp:PpCalculation',
    'quantumespresso.projwfc = aiida_quantumespresso.calculations.projwfc:ProjwfcCalculation',
    'quantumespresso.pw = aiida_quantumespresso.calculations.pw:PwCalculation',
    'quantumespresso.pw2wannier90 = aiida_quantumespresso.calculations.pw2wannier90:Pw2wannier90Calculation',
    'quantumespresso.pwimmigrant = aiida_quantumespresso.calculations.pwimmigrant:PwimmigrantCalculation',
    'quantumespresso.q2r = aiida_quantumespresso.calculations.q2r:Q2rCalculation',
    'raspa = aiida_raspa.calculations:RaspaCalculation',
    'siesta.siesta = aiida_siesta.calculations.siesta:SiestaCalculation',
    'siesta.stm = aiida_siesta.calculations.stm:STMCalculation',
    'vasp.vasp = aiida_vasp.calcs.vasp:VaspCalculation',
    'vasp.vasp2w90 = aiida_vasp.calcs.vasp2w90:Vasp2w90Calculation',
    'wannier90.wannier90 = aiida_wannier90.calculations:Wannier90Calculation',
    'yambo.yambo =  aiida_yambo.calculations.gw:YamboCalculation',
    'zeopp.network = aiida_zeopp.calculations.network:NetworkCalculation',
]


def infer_calculation_entry_point(type_strings):
    """Try to infer a calculation entry point name for all the calculation type strings that are found in the database.

    Before the plugin system was introduced, the `type` column of the node table was a string based on the base node
    type with the module path and class name appended. For example, for the `PwCalculation` class, which was a sub
    class of `JobCalculation`, would get `calculation.job.quantumespresso.pw.PwCalculation.` as its `type` string.
    At this point, the `JobCalculation` also still fullfilled the role of both the `Process` class as well as the
    `Node` class. In the migration for `v1.0.0`, this had to be migrated, where the `type` became that of the actual
    node i.e. `node.process.calculation.calcjob.CalcJobNode.` which would lose the information of which actual sub class
    it represented. This information should be stored in the `process_type` column, where the value is the name of the
    entry point of that calculation class.

    This function will, for a given set of calculation type strings of pre v1.0.0, try to map them on the known entry
    points for the calculation category. This is the union of those entry points registered at the AiiDA registry (see
    the mapping above) and those available in the environment in which this function is ran.

    If a type string cannot be mapped onto an entry point name, a fallback `process_type` string will be generated
    which is based on part of the old `type` string. For example, `calculation.job.unknown.UnknownCalculation.` would
    get the process type string `~unknown.UnknownCalculation`.

    The function will return a mapping of type strings onto their inferred process type strings.

    :param type_strings: a set of type strings whose entry point is to be inferred
    :return: a mapping of current node type string to the inferred entry point name
    """
    from aiida.plugins.entry_point import get_entry_points, parse_entry_point

    prefix_calc_job = 'calculation.job.'
    entry_point_group = 'aiida.calculations'

    entry_point_names = []
    mapping_node_type_to_entry_point = {}

    # Build the list of known entry points, joining those present in the environment with the hard-coded set from taken
    # from the aiida-registry. Note that if entry points with the same name are found in both sets, the entry point
    # from the local environment is kept as leading.
    entry_points_local = get_entry_points(group=entry_point_group)
    entry_points_registry = [
        parse_entry_point(entry_point_group, entry_point) for entry_point in registered_calculation_entry_points
    ]

    entry_points = entry_points_local
    entry_point_names = [entry_point.name for entry_point in entry_points]

    for entry_point in entry_points_registry:
        if entry_point.name not in entry_point_names:
            entry_point_names.append(entry_point.name)

    for type_string in type_strings:
        # If it does not start with the calculation job prefix, it cannot possibly reference a calculation plugin
        if not type_string.startswith(prefix_calc_job):
            continue

        plugin_string = type_string[len(prefix_calc_job) :]
        plugin_parts = [part for part in plugin_string.split('.') if part]
        plugin_class = plugin_parts.pop()
        inferred_entry_point_name = '.'.join(plugin_parts)

        if inferred_entry_point_name in entry_point_names:
            entry_point_string = f'{entry_point_group}:{inferred_entry_point_name}'
        elif inferred_entry_point_name:
            entry_point_string = f'{inferred_entry_point_name}.{plugin_class}'
        else:
            # If there is no inferred entry point name, i.e. there is no module name, use an empty string as fall back
            # This should only be the case for the type string `calculation.job.JobCalculation.`
            entry_point_string = ''

        mapping_node_type_to_entry_point[type_string] = entry_point_string

    return mapping_node_type_to_entry_point


def write_database_integrity_violation(results, headers, reason_message, action_message=None):
    """Emit a integrity violation warning and write the violating records to a log file in the current directory

    :param results: a list of tuples representing the violating records
    :param headers: a tuple of strings that will be used as a header for the log file. Should have the same length
        as each tuple in the results list.
    :param reason_message: a human readable message detailing the reason of the integrity violation
    :param action_message: an optional human readable message detailing a performed action, if any
    """
    from datetime import datetime
    from tempfile import NamedTemporaryFile

    from tabulate import tabulate

    from aiida.manage import configuration

    global_profile = configuration.get_profile()
    if global_profile and global_profile.is_test_profile:
        return

    if action_message is None:
        action_message = 'nothing'

    with NamedTemporaryFile(prefix='migration-', suffix='.log', dir='.', delete=False, mode='w+') as handle:
        LOGGER.warning(
            '\n{}\nFound one or multiple records that violate the integrity of the database\nViolation reason: {}\n'
            'Performed action: {}\nViolators written to: {}\n{}\n'.format(
                WARNING_BORDER, reason_message, action_message, handle.name, WARNING_BORDER
            )
        )

        handle.write(f'# {datetime.utcnow().isoformat()}\n')
        handle.write(f'# Violation reason: {reason_message}\n')
        handle.write(f'# Performed action: {action_message}\n')
        handle.write('\n')
        handle.write(tabulate(results, headers))


def drop_hashes(conn, hash_extra_key: str, entry_point_string: str | None = None) -> None:
    """Drop hashes of nodes.

    Print warning only if the DB actually contains nodes.

    :param hash_extra_key: The key in the extras used to store the hash at the time of this migration.
    :param entry_point_string: Optional entry point string of a node type to narrow the subset of nodes to reset. The
        value should be a complete entry point string, e.g., ``aiida.node:process.calculation.calcjob`` to drop the hash
        of all ``CalcJobNode`` rows.
    """
    from sqlalchemy.sql import text

    from aiida.orm.utils.node import get_type_string_from_class
    from aiida.plugins import load_entry_point_from_string

    if entry_point_string is not None:
        entry_point = load_entry_point_from_string(entry_point_string)
        node_type = get_type_string_from_class(entry_point.__module__, entry_point.__name__)
    else:
        node_type = None

    if node_type:
        statement_count = text(f"SELECT count(*) FROM db_dbnode WHERE node_type = '{node_type}';")
        statement_update = text(
            f"UPDATE db_dbnode SET extras = extras #- '{{{hash_extra_key}}}'::text[]  WHERE node_type = '{node_type}';"
        )
    else:
        statement_count = text('SELECT count(*) FROM db_dbnode;')
        statement_update = text(f"UPDATE db_dbnode SET extras = extras #- '{{{hash_extra_key}}}'::text[];")

    node_count = conn.execute(statement_count).fetchall()[0][0]

    if node_count > 0:
        if entry_point_string:
            msg = f'Invalidating the hashes of certain nodes. Please run `verdi node rehash -e {entry_point_string}`.'
        else:
            msg = 'Invalidating the hashes of all nodes. Please run `verdi node rehash`.'
        LOGGER.warning(msg)

    conn.execute(statement_update)
