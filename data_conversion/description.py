"""
Generates a description.html that will be deposited into the
index.html file. Also generates a boxsize_integer.txt file containing
the box-size converted to Mpc as an integer.

Requires two parameters: path to snapshot, and path to yaml file.
"""

import yaml
from swiftsimio import load

import sys


def latex_float(f):
    float_str = "{0:.4g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str


data = load(sys.argv[1])
with open(sys.argv[2], "r") as handle:
    parameter_file = yaml.load(handle, Loader=yaml.Loader)

with open("boxsize_integer.txt", "w") as handle:
    handle.write("%d" % int(data.metadata.boxsize[0].value + 0.1))

# Now generate HTML
output = f"""<ul>
<li><b>Run Name</b>: {data.metadata.run_name.decode("utf-8").replace('!!python/unicode', '')}</li>
<li><b>Boxsize</b>: {str(data.metadata.boxsize)}</li>
<li><b>Cube root of particle number</b>: {int(data.metadata.n_dark_matter**(1/3)+0.01)}</li>
<li><b>Number of particles at $z={data.metadata.z:2.2f}$</b>:
  <ul>
    <li>Dark matter: {data.metadata.n_dark_matter}</li>
    <li>Gas: {data.metadata.n_gas}</li>
    <li>Star: {data.metadata.n_stars}</li>
    <li>Black hole: {data.metadata.n_black_holes}</li>
  </ul>
</li>
<li><b>Minimal particle masses at $z={data.metadata.z:2.2f}$</b>:
  <ul>
    <li>Dark matter: ${latex_float(data.dark_matter.masses[::100].min().to('Solar_Mass').value)}$ M$_\\odot$</li>
    <li>Gas: ${latex_float(data.gas.masses[::100].min().to('Solar_Mass').value)}$ M$_\\odot$</li>
  </ul>
</li>
<li><b>Particle gravitational softenings</b>:
  <ul>
    <li>Dark matter: {str((float(parameter_file["Gravity"]["max_physical_DM_softening"]) * data.units.length).to('kpc'))}</li>
    <li>Baryons: {str((float(parameter_file["Gravity"]["max_physical_baryon_softening"]) * data.units.length).to('kpc'))}</li>
  </ul>
</li>
<li><b>Code info</b>: {data.metadata.code_info}</li>
<li><b>Compiler info</b>: {data.metadata.compiler_info}</li>
<li><b>Hydrodynamics</b>: {data.metadata.hydro_info}</li>
<li><b>Key parameters</b>:
  <ul>
    <li>$f_{{\\rm E, min}} = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_min']:.4g}$</li>
    <li>$f_{{\\rm E, max}} = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_max']:.4g}$</li>
    <li>$n_Z = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_n_Z']:.4g}$</li>
    <li>$n_0 = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_n_0_H_p_cm3']:.4g}$</li>
    <li>$n_n = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_n_n']:.4g}$</li>
    <li>AGN $\\mathrm{{d}}T = {latex_float(parameter_file['EAGLEAGN']['AGN_delta_T_K'])}$ ($\\log_{{10}}(\\mathrm{{d}}T / K) = {parameter_file['EAGLEAGN']['AGN_delta_T_K']:.4g}$)</li>
    <li>AGN $C_{{\\rm eff}} = {parameter_file['EAGLEAGN']['coupling_efficiency']:.4g}$</li>
    <li>AGN Visocous $\\alpha = {latex_float(parameter_file['EAGLEAGN']['viscous_alpha'])}$</li>
  </ul>
</ul>
"""

with open("description.html", "w") as handle:
    handle.write(output)
