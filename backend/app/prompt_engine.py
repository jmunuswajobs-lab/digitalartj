
from typing import Tuple
from .models import IntensityLevel

# Cluster-specific base prompt templates
# Slots: {pose}, {clothing}, {environment}, {art_variant}
PROMPTS = {
    "C1": {
        "L1": (
            "moody {art_variant} painting of an adult woman in a close, intimate pose, "
            "near-square crop, {pose}, {clothing}, set in {environment}, "
            "soft bare skin suggested by shadows, dim bedroom background, "
            "single warm light source grazing her curves, painterly brushwork, "
            "sensual but restrained, 18+ boudoir illustration, tasteful, non-explicit"
        ),
        "L2": (
            "dark, cinematic {art_variant} painting of an adult woman in a provocative close-crop pose, "
            "near-square framing focusing on the curves of her body and the tension in her posture, "
            "{pose}, {clothing}, {environment}, low-key bedroom lighting with strong contrast, "
            "expression intense and inviting, hyper-detailed skin rendering, "
            "sensual, charged atmosphere, 18+ erotic art, non-explicit"
        ),
        "L3": (
            "high-intensity erotic {art_variant} painting of an adult woman, near-square crop emphasizing sensual curves and dramatic pose, "
            "{pose}, {clothing}, {environment}, harsh directional bedroom light carving out highlights across her figure, "
            "deep blacks and warm saturated highlights, bold confident expression, "
            "18+ erotic artwork, highly suggestive but non-explicit, tasteful composition"
        ),
    },
    "C2": {
        "L1": (
            "bright, soft-focus {art_variant} painting of an adult woman in a playful pose, "
            "near-square crop, {pose}, {clothing}, set in {environment}, "
            "high-key daylight, pastel tones, gentle smile or teasing expression, "
            "boudoir fashion vibe, 18+ audience, sensual but light, non-explicit"
        ),
        "L2": (
            "vibrant {art_variant} illustration of an adult woman in a teasing, provocative pose, "
            "near-square framing, {pose}, {clothing}, {environment}, "
            "strong daylight shaping her figure, warm skin tones against a bright airy background, "
            "expression playful and knowing, 18+ erotic art, non-explicit"
        ),
        "L3": (
            "high-key erotic {art_variant} painting of an adult woman in a bold, flirtatious pose, "
            "near-square crop amplifying curves and posture, {pose}, {clothing}, {environment}, "
            "bright ambient light, glossy highlights on curves, "
            "intensely seductive expression, 18+ erotic illustration, provocative but non-explicit"
        ),
    },
    "C3": {
        "L1": (
            "cinematic portrait {art_variant} painting of an adult woman in a relaxed, sensual pose, "
            "vertical framing from torso up, {pose}, {clothing}, {environment}, "
            "single side light casting dramatic shadows, deep warm shadows, "
            "sensual 18+ boudoir portrait, tasteful, non-explicit"
        ),
        "L2": (
            "dark atmospheric portrait {art_variant} of an adult woman in a confident, provocative pose, "
            "vertical composition, {pose}, {clothing}, {environment}, "
            "strong side lighting chiseling out curves, background fading into near-black, "
            "eyes intense, hyperreal skin rendering, 18+ erotic art, non-explicit"
        ),
        "L3": (
            "intense erotic portrait {art_variant} painting of an adult woman, "
            "vertical framing emphasizing sensual posture and curves, {pose}, {clothing}, {environment}, "
            "hard dramatic light slicing across her figure, deep contrast, "
            "bold, confident expression, 18+ erotic illustration, maximum sensual mood within tasteful limits"
        ),
    },
    "C4": {
        "L1": (
            "soft boudoir portrait {art_variant} painting of an adult woman, "
            "vertical framing from mid-body upward, {pose}, {clothing}, {environment}, "
            "gentle window light, pastel or neutral tones, "
            "romantic sensual 18+ glamour art, tasteful and non-explicit"
        ),
        "L2": (
            "glamorous erotic portrait {art_variant} illustration of an adult woman in a confident pose, "
            "vertical composition, {pose}, {clothing}, {environment}, "
            "strong directional lighting, bold highlights and soft shadows, "
            "high-detail rendering, 18+ erotic glamour art, non-explicit"
        ),
        "L3": (
            "bold luminous erotic portrait {art_variant} painting of an adult woman, "
            "vertical framing emphasizing curves and posture, {pose}, {clothing}, {environment}, "
            "bright sculpting light, subtle background bokeh, "
            "intensely seductive expression, 18+ erotic illustration, highly suggestive but non-explicit"
        ),
    },
    "C5": {
        "L1": (
            "bright boudoir portrait {art_variant} painting of an adult woman, "
            "vertical framing, {pose}, {clothing}, {environment}, "
            "soft daylight, gentle glow on skin, "
            "sensual 18+ glamour art, tasteful, non-explicit"
        ),
        "L2": (
            "glossy fashion-inspired erotic {art_variant} portrait of an adult woman, "
            "vertical composition, {pose}, {clothing}, {environment}, "
            "studio-like lighting with clean highlights, "
            "high-detail rendering, 18+ erotic glamour, non-explicit"
        ),
        "L3": (
            "high-energy erotic fashion {art_variant} portrait of an adult woman, "
            "vertical framing, {pose}, {clothing}, {environment}, "
            "bright directional light, crisp edges and polished look, "
            "confident seductive expression, 18+ illustration, suggestive but non-explicit"
        ),
    },
    "C6": {
        "L1": (
            "full-body boudoir {art_variant} painting of an adult woman reclining in a bedroom setting, "
            "horizontal composition, {pose}, {clothing}, {environment}, "
            "gentle warm light, soft sheets and pillows, "
            "romantic and calm, sensual 18+ art, tasteful, non-explicit"
        ),
        "L2": (
            "cinematic horizontal {art_variant} painting of an adult woman posed provocatively on a bed or couch, "
            "full-body framing with strong diagonals, {pose}, {clothing}, {environment}, "
            "low-key lighting with warm streaks of light, "
            "expression direct and inviting, 18+ erotic illustration, non-explicit"
        ),
        "L3": (
            "high-intensity erotic horizontal {art_variant} artwork of an adult woman in a striking full-body pose, "
            "emphasizing curves while avoiding explicit detail via sheets, fabric or shadow, "
            "{pose}, {clothing}, {environment}, dramatic contrast lighting, "
            "hyperreal digital art look, 18+ erotic painting, bold and very sensual without graphic explicitness"
        ),
    },
}

NEGATIVE_PROMPT = (
    "no minors, no underage, no explicit genitals, no sexual acts, no pornography, "
    "no extreme fetishes, no violence, no injuries, "
    "no deformed hands, no extra limbs, no distorted anatomy, "
    "no watermarks, no text, no logos, no frames, "
    "no low resolution, no heavy blur, no oversharpening, "
    "no bad proportions, no poorly drawn faces"
)

def build_prompt(
    style_family: str,
    intensity: IntensityLevel,
    art_variant: str,
    pose: str,
    clothing: str,
    environment: str,
) -> Tuple[str, str]:
    family = PROMPTS.get(style_family)
    if not family:
        # fallback generic erotic art prompt
        base = (
            "sensual {art_variant} painting of an adult woman, "
            "{pose}, {clothing}, set in {environment}, "
            "romantic intimate lighting, 18+ art, tasteful, non-explicit"
        )
    else:
        base = family[intensity]

    prompt = base.format(
        art_variant=art_variant.replace("_", " "),
        pose=pose,
        clothing=clothing,
        environment=environment,
    )

    return prompt, NEGATIVE_PROMPT
