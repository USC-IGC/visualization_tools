%% Matlab figures for Freesurfer ROIs
	%% Neda Jahanshad 2018 
	%% neda.jahanshad@usc.edu

		
%% need two files, one for RH, one for LH
% csv file of freesurfer regions and their corresponding statistics
resultsR=readtable('resultsfile_RH_zscore.csv');
resultsL=readtable('resultsfile_LH_zscore.csv');

%% user options
semiinflated=0;
colorBarLabel='z-score';
outdir0='';
% to set min and max colors for mapping
colorMin=-5;
colorMax=5;
% flip = 0
% colorscheme = ""


% to threshold and only show values w greater magnitude
zthresh=1.96; 

alpha=1;

FScolors=0;
laptop=1;
% matlab uses your screen's dimensions to set the figsize
% set laptop=0 if you're using a desktop

cortical_measure='SA'; % options are 'TH' or 'SA' --no difference anymore

effectlistR=resultsR.Properties.VariableNames(7:end);
effectlistL=resultsL.Properties.VariableNames(7:end);
N=length(effectlistR);

startN=1;
endN=N;

mkdir(outdir0)


%% get more colors
% https://www.mathworks.com/matlabcentral/fileexchange/30564-othercolor
addpath('./othercolor/othercolor/') ;
warning('off')

%% RH vertices:
if semiinflated == 1
    FScoord=textread(char('RH.pial_semi_inflated.coord.txt')); 
else
FScoord=textread(char('RH.pial.coord.txt')); 
end
Faces=textread(char('RH.pial.faces.txt'));  
X=FScoord(:,1);Y=FScoord(:,2);Z=FScoord(:,3);
FSlabels=textread(char('RH.pial.label.txt')); 
FSlabels6=num2cell(FSlabels(:,1));

%% LH vertices:
if semiinflated == 1
    FScoordL=textread(char('LH.pial_semi_inflated.coord.txt')); 
else
FScoordL=textread(char('LH.pial.coord.txt')); 
end 
FacesL=textread(char('LH.pial.faces.txt'));  
XL=FScoordL(:,1);YL=FScoordL(:,2);ZL=FScoordL(:,3);
FSlabelsL=textread(char('LH.pial.label.txt')); 
FSlabels6L=num2cell(FSlabelsL(:,1));

% same for both hemispheres
ROI_keys=resultsL{:,'label'};

%% loop through columns of results

for i=startN:endN
i
    outfile=char(strcat('brain_',effectlistR(i),'_',colorBarLabel));
    outdir=char(strcat(outdir0,'/',effectlistR(i),'/'));
    mkdir(outdir) 
   
result_column=char(effectlistR(i))
ROI_valuesR=resultsR{:,result_column};
ROI_valuesL=resultsL{:,result_column};

mapObjR=containers.Map('KeyType','double','ValueType','double');
mapObjR=containers.Map(ROI_keys,ROI_valuesR);
mapObjL=containers.Map('KeyType','double','ValueType','double');
mapObjL=containers.Map(ROI_keys,ROI_valuesL);

% map verticies and threshold for R
AAR = values(mapObjR,FSlabels6);
AR=cell2mat(AAR);
ZcolorR=zeros(length(Z),1);
indx=find(abs(AR(:))>=zthresh);
ZcolorR(indx)=alpha;
indxROI=find(abs(AR(:))==0);
ZcolorR(indxROI)=0;

% map verticies and threshold for L
AAL = values(mapObjL,FSlabels6L);
AL=cell2mat(AAL);
ZcolorL=zeros(length(Z),1);
indx2=find(abs(AL(:))>=zthresh);
ZcolorL(indx2)=alpha;
indxROI=find(abs(AL(:))==0);
ZcolorL(indxROI)=0;

%% figure

% right hemisphere on top
h.fig = figure; %('Visible','off'); 
s(1)=subplot('position',[0.05 0.5 0.45 0.4]) ;

h.surf(1)=trisurf(Faces, X, Y, Z, zeros(length(Z),1),...
    'FaceAlpha',1,...
    'EdgeColor','none', ... 
    'LineStyle','none',...
    'facevertexcdata',ones(length(Z),3));

hold on;

h.surf(2) = trisurf(Faces, X, Y, Z,ones(length(Z),1));  
set(h.surf(2),'FaceAlpha','flat','FaceVertexAlphaData',ZcolorR,...
    'facevertexcdata',AR,'FaceColor','flat','AlphaDataMapping','none',...
    'CDataMapping','scaled','EdgeColor',[0.3 0.3 0.3],'EdgeAlpha',0,...
    'Linestyle','--','Linewidth', 0.1);

set(h.surf,'BackFaceLighting','reverselit',...
    'AmbientStrength',0.2, 'DiffuseStrength',0.8,...
    'FaceLighting','gouraud',...
    'EdgeLighting','gouraud',...
    'SpecularColorReflectance', 0.1,... % 0.1,5,0.1
    'SpecularExponent', 5,'SpecularStrength', 0.1);

if (colorMin < 0) 
    colormap(flipud(othercolor('RdBu10')));
    else
    colormap(othercolor('Reds9'));
end  

% if (colorMin < 0)
%   if flip == 1
%       colormap(flipud(othercolor('RdBu10')))
%   end
% end

if (laptop==1)
    screensizeLaptop=get( groot, 'Screensize' );
set(h.fig,'Position',[screensizeLaptop(1) screensizeLaptop(2)...
       screensizeLaptop(3)/2 screensizeLaptop(4)]);
end


caxis([colorMin colorMax])
axis(s(1),'off')
zlabel(s(1),'Right Hemisphere','fontsize',18);
s(1).ZLabel.Visible = 'on';

axis equal
axis tight;
daspect([1 1 1]);
light('position',[1 1 1]);
light('position',[-1 -1 -1]);
view(90,0)
%% %% 
s(2)=subplot('position',[0.52 0.5 0.45 0.4]) ;
h.surf(1)=trisurf(Faces, X, Y, Z, zeros(length(Z),1),...
    'FaceAlpha',1,...
    'EdgeColor','none', ... 
    'LineStyle','none',...
    'facevertexcdata',ones(length(Z),3));

hold on;

h.surf(2) = trisurf(Faces, X, Y, Z,ones(length(Z),1));  
set(h.surf(2),'FaceAlpha','flat','FaceVertexAlphaData',ZcolorR,...
    'facevertexcdata',AR,'FaceColor','flat','AlphaDataMapping','none',...
    'CDataMapping','scaled','EdgeColor',[0.3 0.3 0.3],'EdgeAlpha',0,...
    'Linestyle','--','Linewidth', 0.1);

set(h.surf,'BackFaceLighting','reverselit',...
    'AmbientStrength',0.2, 'DiffuseStrength',0.8,...
    'FaceLighting','gouraud',...
    'EdgeLighting','gouraud',...
    'SpecularColorReflectance', 0.1,... % 0.1,5,0.1
    'SpecularExponent', 5,'SpecularStrength', 0.1);

caxis([colorMin colorMax])
axis off;
axis equal
axis tight;
daspect([1 1 1]);
view(-90,0)
light('position',[1 1 1]);
light('position',[-1 -1 -1]);


%% Left hemisphere

s(3)=subplot('position',[0.05 0.1 0.45 0.4]) ;
h.surf(1)=trisurf(FacesL, XL, YL, ZL, zeros(length(ZL),1),...
    'FaceAlpha',1,...
    'EdgeColor','none', ... 
    'LineStyle','none',...
    'facevertexcdata',ones(length(ZL),3));

hold on;

h.surf(2) = trisurf(FacesL, XL, YL, ZL,zeros(length(ZL),1));  
set(h.surf(2),'FaceAlpha','flat','FaceVertexAlphaData',ZcolorL,...
    'facevertexcdata',AL,'FaceColor','flat','AlphaDataMapping','none',...
    'CDataMapping','scaled','EdgeColor',[0.3 0.3 0.3],'EdgeAlpha',0,...
    'Linestyle','--','Linewidth', 0.1);

set(h.surf,'BackFaceLighting','reverselit',...
    'AmbientStrength',0.2, 'DiffuseStrength',0.8,...
    'FaceLighting','gouraud',...
    'EdgeLighting','gouraud',...
    'SpecularColorReflectance', 0.1,... % 0.1,5,0.1
    'SpecularExponent', 5,'SpecularStrength', 0.1);


caxis([colorMin colorMax])
axis(s(3),'off');
ylabel(s(3),'Lateral View','fontsize',16);
s(3).YLabel.Visible = 'on';
zlabel(s(3),'Left Hemisphere','fontsize',18);
s(3).ZLabel.Visible = 'on';

axis equal
axis tight;
daspect([1 1 1]);
light('position',[1 1 1]);
light('position',[-1 -1 -1]);
view(-90,0)

% plot 2
s(4)=subplot('position',[0.52 0.1 0.45 0.4]) ;
h.surf(1)=trisurf(FacesL, XL, YL, ZL, zeros(length(ZL),1),...
    'FaceAlpha',1,...
    'EdgeColor','none', ... 
    'LineStyle','none',...
    'facevertexcdata',ones(length(ZL),3));

hold on;

h.surf(2) = trisurf(FacesL, XL, YL, ZL,zeros(length(ZL),1));  
set(h.surf(2),'FaceAlpha','flat','FaceVertexAlphaData',ZcolorL,...
    'facevertexcdata',AL,'FaceColor','flat','AlphaDataMapping','none',...
    'CDataMapping','scaled','EdgeColor',[0.3 0.3 0.3],'EdgeAlpha',0,...
    'Linestyle','--','Linewidth', 0.1);

set(h.surf,'BackFaceLighting','reverselit',...
    'AmbientStrength',0.2, 'DiffuseStrength',0.8,...
    'FaceLighting','gouraud',...
    'EdgeLighting','gouraud',...
    'SpecularColorReflectance', 0.1,... % 0.1,5,0.1
    'SpecularExponent', 5,'SpecularStrength', 0.1);

caxis([colorMin colorMax])

axis(s(4),'off');
ylabel(s(4),'Medial View','fontsize',16);
s(4).YLabel.Visible = 'on';

axis equal
axis tight;
daspect([1 1 1]);
light('position',[1 1 1]);
light('position',[-1 -1 -1]);
view(90,0)

%%
saveas(h.fig,char(strcat(outdir,outfile)),'png')

hc=figure('Visible','off'); 
if (colorMin < 0) 
    colormap(flipud(othercolor('RdBu10')));
    else
    colormap(othercolor('Reds9'));
end 

cb=colorbar('southoutside','fontsize',16,'Ticks',colorMin:((colorMax-colorMin)/10):colorMax);caxis([colorMin colorMax]); 
cb.Label.String = colorBarLabel;
%set(cb,'fontsize',20)
axis off
saveas(hc,char(strcat(outdir,outfile,'scale',num2str(colorMin),'_',num2str(colorMax),'color_bar.pdf')),'pdf')
hold off;
%close all; %clear all;
end
