import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import IPython.display as ipd
import pytest

from qpiai_quantum.circuit import Circuit
from qpiai_quantum.icr.circuitoperation import Operation
from qpiai_quantum.visualization.matplotlib_visualizer.plotter import Plotter
from qpiai_quantum.visualization.matplotlib_visualizer.visualizer import (
    MatplotlibVisualizer,
)


def build_sample_visualization_circuit():
    circuit = Circuit(2, 2)
    circuit.sdg(0)
    circuit.cp(0, 1, 0.79)
    circuit.add_operation(Operation(r"\theta_1", [0, 1]))
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def test_plotter_formats_mathtext_labels():
    plotter = Plotter(4, 2, 16, 1, use_mathtext=True)
    plotter.draw_qubit_wires(0, 3, 2)
    plotter.draw_one_qubit_non_parametric(1, 0, "Sdg")
    plotter.draw_one_qubit_parametric(2, 1, "RX", "0.79")
    plotter.draw_measure(3, 0, 2, 0)

    labels = {text.get_text() for text in plotter.ax.texts}

    assert "$\\mathrm{q}_{0}$" in labels
    assert "$\\mathrm{S}^{\\dagger}$" in labels
    assert "$\\mathrm{RX}_{0.79}$" in labels
    assert "$\\mathrm{c}_{0}$" in labels

    plt.close(plotter.fig)


def test_plotter_uses_bolder_gate_style():
    plotter = Plotter(4, 2, 16, 1, use_mathtext=True)
    plotter.draw_one_qubit_non_parametric(1, 0, "Sdg")
    plotter.draw_two_qubit_non_parametric(2, 0, 1, "X")

    one_qubit_box = plotter.ax.patches[0]
    control_dot = plotter.ax.patches[1]
    controlled_target = plotter.ax.patches[2]
    gate_labels = plotter.ax.texts

    assert one_qubit_box.get_linewidth() == pytest.approx(plotter.gate_linewidth)
    assert controlled_target.get_linewidth() == pytest.approx(plotter.gate_linewidth)
    assert control_dot.get_facecolor() == pytest.approx(
        (36 / 255, 94 / 255, 175 / 255, 1)
    )
    assert all(text.get_fontsize() == plotter.gate_font_size for text in gate_labels)
    assert all(text.get_path_effects() for text in gate_labels)

    plt.close(plotter.fig)


def test_plotter_formats_simple_greek_labels_without_math_italics():
    plotter = Plotter(4, 2, 16, 1, use_mathtext=True)
    plotter.draw_multi_qubit_gate(1, [0, 1], r"\theta_1")

    assert plotter.ax.texts[0].get_text() == r"θ$_{1}$"

    plt.close(plotter.fig)


def test_plotter_can_preserve_legacy_labels():
    plotter = Plotter(2, 1, 16, 1, use_mathtext=False)
    plotter.draw_one_qubit_non_parametric(1, 0, "Sdg")

    assert plotter.ax.texts[0].get_text() == "Sdg"

    plt.close(plotter.fig)


def test_visualizer_only_rewrites_known_controlled_gate_labels():
    assert MatplotlibVisualizer._target_gate_label("CX") == "X"
    assert MatplotlibVisualizer._target_gate_label("CP") == "P"
    assert MatplotlibVisualizer._target_gate_label("Custom") == "Custom"


def test_circuit_show_forwards_mathtext_flag(monkeypatch):
    captured = {}

    def fake_plot_icr(icr, theme="light", dpi=200, use_mathtext=True):
        captured["icr"] = icr
        captured["theme"] = theme
        captured["dpi"] = dpi
        captured["use_mathtext"] = use_mathtext

    monkeypatch.setattr(MatplotlibVisualizer, "plot_icr", staticmethod(fake_plot_icr))

    circuit = Circuit(1)
    circuit.show(theme="dark", dpi=144, use_mathtext=False)

    assert captured["icr"] is circuit.icr
    assert captured["theme"] == "dark"
    assert captured["dpi"] == 144
    assert captured["use_mathtext"] is False


def test_visualizer_handles_fractional_operation_positions(monkeypatch):
    circuit = build_sample_visualization_circuit()

    rendered = []

    def capture_display(obj, *args, **kwargs):
        rendered.append(obj)

    monkeypatch.setattr(ipd, "display", capture_display)

    circuit.show(use_mathtext=True)

    assert rendered


def test_operation_width_keeps_plain_text_rule():
    # ThetaGate is 9 chars -> 4 * 0.5 + 5 * 0.2 = 3.0 units
    assert Plotter.operation_width_for_label("ThetaGate") == pytest.approx(3.0 * 0.65)


def test_operation_width_compacts_mathtext_source():
    mathtext_width = Plotter.operation_width_for_label(r"\theta_1", use_mathtext=True)
    raw_width = Plotter.operation_width_for_label(r"\theta_1", use_mathtext=False)

    # mathtext evaluates to \theta (0.5) + _1 (0.35). units = 0.85 -> max(1.0) -> width = 0.65
    assert mathtext_width == pytest.approx(0.65)
    # raw \theta_1 processes \t, h, e, t, a, _, 1 (7 logical characters)
    # 4 * 0.5 + 3 * 0.8 = 4.4 units -> width = 2.86
    assert raw_width == pytest.approx(4.4 * 0.65)
    assert mathtext_width < raw_width


def test_custom_operation_uses_shared_width_and_spacing_rule():
    label = r"\theta_1"
    plotter = Plotter(4, 2, 16, 1, use_mathtext=True)
    plotter.draw_multi_qubit_gate(2, [0, 1], label)

    rect = plotter.ax.patches[0]
    width = Plotter.operation_width_for_label(label)

    assert rect.get_width() == pytest.approx(width)
    assert width == pytest.approx(0.65)
    assert Plotter.operation_column_width_for_label(label) == pytest.approx(
        width + Plotter.CUSTOM_OPERATION_PADDING
    )
    assert rect.get_x() == pytest.approx(2 - width / 2)
    assert plotter.ax.texts[0].get_position()[0] == pytest.approx(2)

    plt.close(plotter.fig)
