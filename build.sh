#!/bin/sh

set -e -x

output_dir=$PWD/io
mkdir -p ${output_dir}

rm -rf /tmp/build_presentation
mkdir -p /tmp/build_presentation

if test "$#" -eq 1
then
  main_files=$1
else
  main_files=`grep -lr '\\documentclass' . | grep tex$`
fi

for main_file in ${main_files}
do
  abs_source_dir=`dirname ${main_file}`
  rel_source_dir=`basename ${abs_source_dir}`
  source_file=`basename ${main_file}`
  binary_file=`echo ${source_file} | sed "s|.tex|.pdf|g"`
  echo "-- Compiling ${main_file} --"
  cp -rv ${abs_source_dir} /tmp/build_presentation
  cd /tmp/build_presentation/${rel_source_dir}
  pdflatex --halt-on-error ${source_file}
  pdflatex ${source_file}
  pdflatex ${source_file}
  cp -v ${binary_file} ${output_dir}
  cd -
done

