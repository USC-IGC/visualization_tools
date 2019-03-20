% -------------------------------------------------------------------
%  Fabrizio Pizzagalli
%  March 18 2019
% -------------------------------------------------------------------
load('so_fp.mat');

so.img(1)    

so.img(1).vol.fname='avg152T1.nii' %Structual Image
so.img(2).vol.fname='Figure1A-Controls_vs_Patients-VBM-GreyMatter.nii' %Statistical Map
so.slices=[-22:1:-18] %Slices to visualize

%Axial view
M_axial = eye(4,4)

%Coronal Matrix
M_coronal = zeros(4,4)
M_coronal(1,:) = [1 0 0 0]
M_coronal(2,:) = [0 -0.0000 1.0000 0]
M_coronal(3,:) = [0 1.0000 0.0000 0]
M_coronal(4,:) = [0 0 0 1]

%Sagittal Matrix
M_sag = zeros(4,4)
M_sag(1,:) = [-0 -1 0 0]
M_sag(2,:) = [-0 0.0000 1.0000 0]
M_sag(3,:) = [1 -0.0000 0.0000 0]
M_sag(4,:) = [0 0 0 1]

so.transform = M_axial;

so=paint(so) %to reopen with the new parameters