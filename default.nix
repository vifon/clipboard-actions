{ pkgs ? import <nixpkgs> {} }:

with pkgs;
with python3Packages;
buildPythonApplication rec {
  pname = "clipboard-actions";
  version = "0.9";
  src = lib.cleanSource ./.;

  propagatedBuildInputs = [
    httpx xsel xclip dmenu
  ];
}
